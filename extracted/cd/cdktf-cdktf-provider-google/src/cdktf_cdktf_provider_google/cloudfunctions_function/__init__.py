r'''
# `google_cloudfunctions_function`

Refer to the Terraform Registry for docs: [`google_cloudfunctions_function`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function).
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


class CloudfunctionsFunction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunction",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function google_cloudfunctions_function}.'''

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
        event_trigger: typing.Optional[typing.Union["CloudfunctionsFunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
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
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        source_archive_bucket: typing.Optional[builtins.str] = None,
        source_archive_object: typing.Optional[builtins.str] = None,
        source_repository: typing.Optional[typing.Union["CloudfunctionsFunctionSourceRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CloudfunctionsFunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function google_cloudfunctions_function} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A user-defined name of the function. Function names must be unique globally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#name CloudfunctionsFunction#name}
        :param runtime: The runtime in which the function is going to run. Eg. "nodejs20", "python37", "go111". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#runtime CloudfunctionsFunction#runtime}
        :param available_memory_mb: Memory (in MB), available to the function. Default value is 256. Possible values include 128, 256, 512, 1024, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#available_memory_mb CloudfunctionsFunction#available_memory_mb}
        :param build_environment_variables: A set of key/value environment variable pairs available during build time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_environment_variables CloudfunctionsFunction#build_environment_variables}
        :param build_service_account: The fully-qualified name of the service account to be used for the build step of deploying this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_service_account CloudfunctionsFunction#build_service_account}
        :param build_worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_worker_pool CloudfunctionsFunction#build_worker_pool}
        :param description: Description of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#description CloudfunctionsFunction#description}
        :param docker_registry: Docker Registry to use for storing the function's Docker images. Allowed values are ARTIFACT_REGISTRY (default) and CONTAINER_REGISTRY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#docker_registry CloudfunctionsFunction#docker_registry}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. If specified, deployments will use Artifact Registry for storing images built with Cloud Build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#docker_repository CloudfunctionsFunction#docker_repository}
        :param entry_point: Name of the function that will be executed when the Google Cloud Function is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#entry_point CloudfunctionsFunction#entry_point}
        :param environment_variables: A set of key/value environment variable pairs to assign to the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#environment_variables CloudfunctionsFunction#environment_variables}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#event_trigger CloudfunctionsFunction#event_trigger}
        :param https_trigger_security_level: The security level for the function. Defaults to SECURE_OPTIONAL. Valid only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#https_trigger_security_level CloudfunctionsFunction#https_trigger_security_level}
        :param https_trigger_url: URL which triggers function execution. Returned only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#https_trigger_url CloudfunctionsFunction#https_trigger_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#id CloudfunctionsFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_settings: String value that controls what traffic can reach the function. Allowed values are ALLOW_ALL and ALLOW_INTERNAL_ONLY. Changes to this field will recreate the cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#ingress_settings CloudfunctionsFunction#ingress_settings}
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#kms_key_name CloudfunctionsFunction#kms_key_name}
        :param labels: A set of key/value label pairs to assign to the function. Label keys must follow the requirements at https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#labels CloudfunctionsFunction#labels}
        :param max_instances: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#max_instances CloudfunctionsFunction#max_instances}
        :param min_instances: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#min_instances CloudfunctionsFunction#min_instances}
        :param project: Project of the function. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#project CloudfunctionsFunction#project}
        :param region: Region of function. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#region CloudfunctionsFunction#region}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret_environment_variables CloudfunctionsFunction#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret_volumes CloudfunctionsFunction#secret_volumes}
        :param service_account_email: If provided, the self-provided service account to run the function with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#service_account_email CloudfunctionsFunction#service_account_email}
        :param source_archive_bucket: The GCS bucket containing the zip archive which contains the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_archive_bucket CloudfunctionsFunction#source_archive_bucket}
        :param source_archive_object: The source archive object (file) in archive bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_archive_object CloudfunctionsFunction#source_archive_object}
        :param source_repository: source_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_repository CloudfunctionsFunction#source_repository}
        :param timeout: Timeout (in seconds) for the function. Default value is 60 seconds. Cannot be more than 540 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#timeout CloudfunctionsFunction#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#timeouts CloudfunctionsFunction#timeouts}
        :param trigger_http: Boolean variable. Any HTTP request (of a supported type) to the endpoint will trigger function execution. Supported HTTP request types are: POST, PUT, GET, DELETE, and OPTIONS. Endpoint is returned as https_trigger_url. Cannot be used with trigger_bucket and trigger_topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#trigger_http CloudfunctionsFunction#trigger_http}
        :param vpc_connector: The VPC Network Connector that this cloud function can connect to. It can be either the fully-qualified URI, or the short name of the network connector resource. The format of this field is projects/* /locations/* /connectors/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#vpc_connector CloudfunctionsFunction#vpc_connector} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param vpc_connector_egress_settings: The egress settings for the connector, controlling what traffic is diverted through it. Allowed values are ALL_TRAFFIC and PRIVATE_RANGES_ONLY. Defaults to PRIVATE_RANGES_ONLY. If unset, this field preserves the previously set value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#vpc_connector_egress_settings CloudfunctionsFunction#vpc_connector_egress_settings}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a89ecd4c85b9f139b8aa86d6db733fc68643fd1ba20f9fed4cced0a019867d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudfunctionsFunctionConfig(
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
        '''Generates CDKTF code for importing a CloudfunctionsFunction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudfunctionsFunction to import.
        :param import_from_id: The id of the existing CloudfunctionsFunction that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudfunctionsFunction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0433b725b3bb85308b11cb46ad410115d690a34d86d338d616ab4c7aeb6dd6a2)
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
        failure_policy: typing.Optional[typing.Union["CloudfunctionsFunctionEventTriggerFailurePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event_type: The type of event to observe. For example: "google.storage.object.finalize". See the documentation on calling Cloud Functions for a full reference of accepted triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#event_type CloudfunctionsFunction#event_type}
        :param resource: The name or partial URI of the resource from which to observe events. For example, "myBucket" or "projects/my-project/topics/my-topic". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#resource CloudfunctionsFunction#resource}
        :param failure_policy: failure_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#failure_policy CloudfunctionsFunction#failure_policy}
        '''
        value = CloudfunctionsFunctionEventTrigger(
            event_type=event_type, resource=resource, failure_policy=failure_policy
        )

        return typing.cast(None, jsii.invoke(self, "putEventTrigger", [value]))

    @jsii.member(jsii_name="putSecretEnvironmentVariables")
    def put_secret_environment_variables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cfe612170de2240536f6c63fddb0ffe95335f4b8a69b35c5734a719b321ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretEnvironmentVariables", [value]))

    @jsii.member(jsii_name="putSecretVolumes")
    def put_secret_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3a49df0dfed6908175e29739658509f97c119c2579a4cf7a2314af7943369f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecretVolumes", [value]))

    @jsii.member(jsii_name="putSourceRepository")
    def put_source_repository(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL pointing to the hosted repository where the function is defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#url CloudfunctionsFunction#url}
        '''
        value = CloudfunctionsFunctionSourceRepository(url=url)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#create CloudfunctionsFunction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#delete CloudfunctionsFunction#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#read CloudfunctionsFunction#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#update CloudfunctionsFunction#update}.
        '''
        value = CloudfunctionsFunctionTimeouts(
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
    def event_trigger(self) -> "CloudfunctionsFunctionEventTriggerOutputReference":
        return typing.cast("CloudfunctionsFunctionEventTriggerOutputReference", jsii.get(self, "eventTrigger"))

    @builtins.property
    @jsii.member(jsii_name="secretEnvironmentVariables")
    def secret_environment_variables(
        self,
    ) -> "CloudfunctionsFunctionSecretEnvironmentVariablesList":
        return typing.cast("CloudfunctionsFunctionSecretEnvironmentVariablesList", jsii.get(self, "secretEnvironmentVariables"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumes")
    def secret_volumes(self) -> "CloudfunctionsFunctionSecretVolumesList":
        return typing.cast("CloudfunctionsFunctionSecretVolumesList", jsii.get(self, "secretVolumes"))

    @builtins.property
    @jsii.member(jsii_name="sourceRepository")
    def source_repository(
        self,
    ) -> "CloudfunctionsFunctionSourceRepositoryOutputReference":
        return typing.cast("CloudfunctionsFunctionSourceRepositoryOutputReference", jsii.get(self, "sourceRepository"))

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
    def timeouts(self) -> "CloudfunctionsFunctionTimeoutsOutputReference":
        return typing.cast("CloudfunctionsFunctionTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["CloudfunctionsFunctionEventTrigger"]:
        return typing.cast(typing.Optional["CloudfunctionsFunctionEventTrigger"], jsii.get(self, "eventTriggerInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretEnvironmentVariables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretEnvironmentVariables"]]], jsii.get(self, "secretEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVolumesInput")
    def secret_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumes"]]], jsii.get(self, "secretVolumesInput"))

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
    ) -> typing.Optional["CloudfunctionsFunctionSourceRepository"]:
        return typing.cast(typing.Optional["CloudfunctionsFunctionSourceRepository"], jsii.get(self, "sourceRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudfunctionsFunctionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudfunctionsFunctionTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0032effa2dca76f1475fede909fbe1687c873574ad902418945e9e1cca21d662)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74baee3f9f62407776543ef761c0049263caa5bb61ec4ee6b3689be24d696144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildEnvironmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildServiceAccount")
    def build_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildServiceAccount"))

    @build_service_account.setter
    def build_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93965384f07f6de63774cf3baa6779a8eea3fcb375eebb0e3f3fd6c78b56e766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildWorkerPool")
    def build_worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildWorkerPool"))

    @build_worker_pool.setter
    def build_worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a853b4325513d67681dca7f9a5c86fe1073f62f494e10bdfa56a4b326ef8e78b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildWorkerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b6b2035a9c2fc73952fd4020edebac36bd8f2685316f37b263edd02d303a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerRegistry")
    def docker_registry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerRegistry"))

    @docker_registry.setter
    def docker_registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9299a352e7764b5a79723885756a2a82504d87b5b0e3da4be8e6e55a15936861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRegistry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerRepository")
    def docker_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerRepository"))

    @docker_repository.setter
    def docker_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e43e2c211fc4068574c7cc4b1c9509356d4ccb1f6b466da27f4e29274e5ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entryPoint")
    def entry_point(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entryPoint"))

    @entry_point.setter
    def entry_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627aace216a71caf3f59b45a35d0bd560371dd2d75947d56a54a12b7207f523a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e99dec82bc16241ae4e139ee604bcdd3de4b82c9437aed42fe3b37ba05708a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsTriggerSecurityLevel")
    def https_trigger_security_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsTriggerSecurityLevel"))

    @https_trigger_security_level.setter
    def https_trigger_security_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb17d89266a116318ea9bf7f7f6d6cde546c695ae99c6482448b567a59fc893e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsTriggerSecurityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsTriggerUrl")
    def https_trigger_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsTriggerUrl"))

    @https_trigger_url.setter
    def https_trigger_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c14a7f5a2fdf2d75e51d8c78f3a035fa46eddd2852d8baab77c5636a0f216c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsTriggerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7520e3b0364fb6476d9584147c240b165b6e7cb2b9eac70e817167e82157c568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressSettings")
    def ingress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressSettings"))

    @ingress_settings.setter
    def ingress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0459e47c574c6008b0da3225d48ad0d92452d59034460e31dc44897b6431c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d942088928fd6a3949ff4c930eb268cd58fc74f4df04c365c876cceb57d21f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74677ce7e89ac4c038b5b29ed9dffb0dc9997cd0aa0daabbd9d7e44957cc202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f6cd1de3aa9b75529340c8e257c437f79be3563f45e170311866b6d1a0f3b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @min_instances.setter
    def min_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30623a7297a659a2cc9c79211d9f4b962ad3ed6c42d6a0edf05b175d86461279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1e07dd3f3a59bc57aa882d28589a311ea22c11b9b6873a103d7ef0d92e68e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e91718ed43fe495b52c15b4b89721a5a6a5c3be0487cb670928aa2f502eb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc773c3cf635ce86acdcf7ecd5be7fdb562b2a0ffcdd6f042cc1a37eb245e330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e721c991a487d7fcfcbac469882f6833a584c73dd2799689162fdb1f1b6970f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmail")
    def service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmail"))

    @service_account_email.setter
    def service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c897f8c651b389e687c7da7aca5c05723540a879fc95b2e618c7191a23fb56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceArchiveBucket")
    def source_archive_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceArchiveBucket"))

    @source_archive_bucket.setter
    def source_archive_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8875ac83a3b4369daeaf3d3bea06a1becff3b8e1bcd90d6df81e9e98effe29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArchiveBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceArchiveObject")
    def source_archive_object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceArchiveObject"))

    @source_archive_object.setter
    def source_archive_object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293561b179a5288767701ddb3908f7f8e3f787cd9f1e43f19f53fe8252026475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArchiveObject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5996631f71c287a90f5e518154adf0d243272ede0afec36403f2b232b7b0eb9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b71a5ce18f08b7cfc2583dfff1b05a21fe12b5535c3321ae5f3a6e2251d42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerHttp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnector")
    def vpc_connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnector"))

    @vpc_connector.setter
    def vpc_connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02eb0f40ff668a0d603d76dd0be0ff9b5d5c77b7ca0a0ca43a6910ab7e167da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcConnectorEgressSettings")
    def vpc_connector_egress_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectorEgressSettings"))

    @vpc_connector_egress_settings.setter
    def vpc_connector_egress_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a506147f50af40675a444b8fdd52d9c93616ec83cc44d5ad4a633294bd58331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectorEgressSettings", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionConfig",
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
class CloudfunctionsFunctionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        event_trigger: typing.Optional[typing.Union["CloudfunctionsFunctionEventTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
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
        secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretEnvironmentVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account_email: typing.Optional[builtins.str] = None,
        source_archive_bucket: typing.Optional[builtins.str] = None,
        source_archive_object: typing.Optional[builtins.str] = None,
        source_repository: typing.Optional[typing.Union["CloudfunctionsFunctionSourceRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["CloudfunctionsFunctionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: A user-defined name of the function. Function names must be unique globally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#name CloudfunctionsFunction#name}
        :param runtime: The runtime in which the function is going to run. Eg. "nodejs20", "python37", "go111". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#runtime CloudfunctionsFunction#runtime}
        :param available_memory_mb: Memory (in MB), available to the function. Default value is 256. Possible values include 128, 256, 512, 1024, etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#available_memory_mb CloudfunctionsFunction#available_memory_mb}
        :param build_environment_variables: A set of key/value environment variable pairs available during build time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_environment_variables CloudfunctionsFunction#build_environment_variables}
        :param build_service_account: The fully-qualified name of the service account to be used for the build step of deploying this function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_service_account CloudfunctionsFunction#build_service_account}
        :param build_worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_worker_pool CloudfunctionsFunction#build_worker_pool}
        :param description: Description of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#description CloudfunctionsFunction#description}
        :param docker_registry: Docker Registry to use for storing the function's Docker images. Allowed values are ARTIFACT_REGISTRY (default) and CONTAINER_REGISTRY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#docker_registry CloudfunctionsFunction#docker_registry}
        :param docker_repository: User managed repository created in Artifact Registry optionally with a customer managed encryption key. If specified, deployments will use Artifact Registry for storing images built with Cloud Build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#docker_repository CloudfunctionsFunction#docker_repository}
        :param entry_point: Name of the function that will be executed when the Google Cloud Function is triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#entry_point CloudfunctionsFunction#entry_point}
        :param environment_variables: A set of key/value environment variable pairs to assign to the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#environment_variables CloudfunctionsFunction#environment_variables}
        :param event_trigger: event_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#event_trigger CloudfunctionsFunction#event_trigger}
        :param https_trigger_security_level: The security level for the function. Defaults to SECURE_OPTIONAL. Valid only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#https_trigger_security_level CloudfunctionsFunction#https_trigger_security_level}
        :param https_trigger_url: URL which triggers function execution. Returned only if trigger_http is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#https_trigger_url CloudfunctionsFunction#https_trigger_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#id CloudfunctionsFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_settings: String value that controls what traffic can reach the function. Allowed values are ALLOW_ALL and ALLOW_INTERNAL_ONLY. Changes to this field will recreate the cloud function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#ingress_settings CloudfunctionsFunction#ingress_settings}
        :param kms_key_name: Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#kms_key_name CloudfunctionsFunction#kms_key_name}
        :param labels: A set of key/value label pairs to assign to the function. Label keys must follow the requirements at https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#labels CloudfunctionsFunction#labels}
        :param max_instances: The limit on the maximum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#max_instances CloudfunctionsFunction#max_instances}
        :param min_instances: The limit on the minimum number of function instances that may coexist at a given time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#min_instances CloudfunctionsFunction#min_instances}
        :param project: Project of the function. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#project CloudfunctionsFunction#project}
        :param region: Region of function. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#region CloudfunctionsFunction#region}
        :param secret_environment_variables: secret_environment_variables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret_environment_variables CloudfunctionsFunction#secret_environment_variables}
        :param secret_volumes: secret_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret_volumes CloudfunctionsFunction#secret_volumes}
        :param service_account_email: If provided, the self-provided service account to run the function with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#service_account_email CloudfunctionsFunction#service_account_email}
        :param source_archive_bucket: The GCS bucket containing the zip archive which contains the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_archive_bucket CloudfunctionsFunction#source_archive_bucket}
        :param source_archive_object: The source archive object (file) in archive bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_archive_object CloudfunctionsFunction#source_archive_object}
        :param source_repository: source_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_repository CloudfunctionsFunction#source_repository}
        :param timeout: Timeout (in seconds) for the function. Default value is 60 seconds. Cannot be more than 540 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#timeout CloudfunctionsFunction#timeout}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#timeouts CloudfunctionsFunction#timeouts}
        :param trigger_http: Boolean variable. Any HTTP request (of a supported type) to the endpoint will trigger function execution. Supported HTTP request types are: POST, PUT, GET, DELETE, and OPTIONS. Endpoint is returned as https_trigger_url. Cannot be used with trigger_bucket and trigger_topic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#trigger_http CloudfunctionsFunction#trigger_http}
        :param vpc_connector: The VPC Network Connector that this cloud function can connect to. It can be either the fully-qualified URI, or the short name of the network connector resource. The format of this field is projects/* /locations/* /connectors/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#vpc_connector CloudfunctionsFunction#vpc_connector} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param vpc_connector_egress_settings: The egress settings for the connector, controlling what traffic is diverted through it. Allowed values are ALL_TRAFFIC and PRIVATE_RANGES_ONLY. Defaults to PRIVATE_RANGES_ONLY. If unset, this field preserves the previously set value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#vpc_connector_egress_settings CloudfunctionsFunction#vpc_connector_egress_settings}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(event_trigger, dict):
            event_trigger = CloudfunctionsFunctionEventTrigger(**event_trigger)
        if isinstance(source_repository, dict):
            source_repository = CloudfunctionsFunctionSourceRepository(**source_repository)
        if isinstance(timeouts, dict):
            timeouts = CloudfunctionsFunctionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4631a97f603e2728b49d8c2d5949bfc3d7cd5d63fd513639b81a9c1aa306429)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#name CloudfunctionsFunction#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''The runtime in which the function is going to run. Eg. "nodejs20", "python37", "go111".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#runtime CloudfunctionsFunction#runtime}
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def available_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''Memory (in MB), available to the function. Default value is 256. Possible values include 128, 256, 512, 1024, etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#available_memory_mb CloudfunctionsFunction#available_memory_mb}
        '''
        result = self._values.get("available_memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def build_environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value environment variable pairs available during build time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_environment_variables CloudfunctionsFunction#build_environment_variables}
        '''
        result = self._values.get("build_environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def build_service_account(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified name of the service account to be used for the build step of deploying this function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_service_account CloudfunctionsFunction#build_service_account}
        '''
        result = self._values.get("build_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_worker_pool(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Build Custom Worker Pool that should be used to build the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#build_worker_pool CloudfunctionsFunction#build_worker_pool}
        '''
        result = self._values.get("build_worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#description CloudfunctionsFunction#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_registry(self) -> typing.Optional[builtins.str]:
        '''Docker Registry to use for storing the function's Docker images. Allowed values are ARTIFACT_REGISTRY (default) and CONTAINER_REGISTRY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#docker_registry CloudfunctionsFunction#docker_registry}
        '''
        result = self._values.get("docker_registry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_repository(self) -> typing.Optional[builtins.str]:
        '''User managed repository created in Artifact Registry optionally with a customer managed encryption key.

        If specified, deployments will use Artifact Registry for storing images built with Cloud Build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#docker_repository CloudfunctionsFunction#docker_repository}
        '''
        result = self._values.get("docker_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry_point(self) -> typing.Optional[builtins.str]:
        '''Name of the function that will be executed when the Google Cloud Function is triggered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#entry_point CloudfunctionsFunction#entry_point}
        '''
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value environment variable pairs to assign to the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#environment_variables CloudfunctionsFunction#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def event_trigger(self) -> typing.Optional["CloudfunctionsFunctionEventTrigger"]:
        '''event_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#event_trigger CloudfunctionsFunction#event_trigger}
        '''
        result = self._values.get("event_trigger")
        return typing.cast(typing.Optional["CloudfunctionsFunctionEventTrigger"], result)

    @builtins.property
    def https_trigger_security_level(self) -> typing.Optional[builtins.str]:
        '''The security level for the function. Defaults to SECURE_OPTIONAL. Valid only if trigger_http is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#https_trigger_security_level CloudfunctionsFunction#https_trigger_security_level}
        '''
        result = self._values.get("https_trigger_security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_trigger_url(self) -> typing.Optional[builtins.str]:
        '''URL which triggers function execution. Returned only if trigger_http is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#https_trigger_url CloudfunctionsFunction#https_trigger_url}
        '''
        result = self._values.get("https_trigger_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#id CloudfunctionsFunction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_settings(self) -> typing.Optional[builtins.str]:
        '''String value that controls what traffic can reach the function.

        Allowed values are ALLOW_ALL and ALLOW_INTERNAL_ONLY. Changes to this field will recreate the cloud function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#ingress_settings CloudfunctionsFunction#ingress_settings}
        '''
        result = self._values.get("ingress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Resource name of a KMS crypto key (managed by the user) used to encrypt/decrypt function resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#kms_key_name CloudfunctionsFunction#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to the function. Label keys must follow the requirements at https://cloud.google.com/resource-manager/docs/creating-managing-labels#requirements.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#labels CloudfunctionsFunction#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_instances(self) -> typing.Optional[jsii.Number]:
        '''The limit on the maximum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#max_instances CloudfunctionsFunction#max_instances}
        '''
        result = self._values.get("max_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''The limit on the minimum number of function instances that may coexist at a given time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#min_instances CloudfunctionsFunction#min_instances}
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Project of the function. If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#project CloudfunctionsFunction#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region of function. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#region CloudfunctionsFunction#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretEnvironmentVariables"]]]:
        '''secret_environment_variables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret_environment_variables CloudfunctionsFunction#secret_environment_variables}
        '''
        result = self._values.get("secret_environment_variables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretEnvironmentVariables"]]], result)

    @builtins.property
    def secret_volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumes"]]]:
        '''secret_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret_volumes CloudfunctionsFunction#secret_volumes}
        '''
        result = self._values.get("secret_volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumes"]]], result)

    @builtins.property
    def service_account_email(self) -> typing.Optional[builtins.str]:
        '''If provided, the self-provided service account to run the function with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#service_account_email CloudfunctionsFunction#service_account_email}
        '''
        result = self._values.get("service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_archive_bucket(self) -> typing.Optional[builtins.str]:
        '''The GCS bucket containing the zip archive which contains the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_archive_bucket CloudfunctionsFunction#source_archive_bucket}
        '''
        result = self._values.get("source_archive_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_archive_object(self) -> typing.Optional[builtins.str]:
        '''The source archive object (file) in archive bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_archive_object CloudfunctionsFunction#source_archive_object}
        '''
        result = self._values.get("source_archive_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_repository(
        self,
    ) -> typing.Optional["CloudfunctionsFunctionSourceRepository"]:
        '''source_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#source_repository CloudfunctionsFunction#source_repository}
        '''
        result = self._values.get("source_repository")
        return typing.cast(typing.Optional["CloudfunctionsFunctionSourceRepository"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for the function. Default value is 60 seconds. Cannot be more than 540 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#timeout CloudfunctionsFunction#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudfunctionsFunctionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#timeouts CloudfunctionsFunction#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudfunctionsFunctionTimeouts"], result)

    @builtins.property
    def trigger_http(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean variable.

        Any HTTP request (of a supported type) to the endpoint will trigger function execution. Supported HTTP request types are: POST, PUT, GET, DELETE, and OPTIONS. Endpoint is returned as https_trigger_url. Cannot be used with trigger_bucket and trigger_topic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#trigger_http CloudfunctionsFunction#trigger_http}
        '''
        result = self._values.get("trigger_http")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vpc_connector(self) -> typing.Optional[builtins.str]:
        '''The VPC Network Connector that this cloud function can connect to.

        It can be either the fully-qualified URI, or the short name of the network connector resource. The format of this field is projects/* /locations/* /connectors/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#vpc_connector CloudfunctionsFunction#vpc_connector}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("vpc_connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_connector_egress_settings(self) -> typing.Optional[builtins.str]:
        '''The egress settings for the connector, controlling what traffic is diverted through it.

        Allowed values are ALL_TRAFFIC and PRIVATE_RANGES_ONLY. Defaults to PRIVATE_RANGES_ONLY. If unset, this field preserves the previously set value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#vpc_connector_egress_settings CloudfunctionsFunction#vpc_connector_egress_settings}
        '''
        result = self._values.get("vpc_connector_egress_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionEventTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "resource": "resource",
        "failure_policy": "failurePolicy",
    },
)
class CloudfunctionsFunctionEventTrigger:
    def __init__(
        self,
        *,
        event_type: builtins.str,
        resource: builtins.str,
        failure_policy: typing.Optional[typing.Union["CloudfunctionsFunctionEventTriggerFailurePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event_type: The type of event to observe. For example: "google.storage.object.finalize". See the documentation on calling Cloud Functions for a full reference of accepted triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#event_type CloudfunctionsFunction#event_type}
        :param resource: The name or partial URI of the resource from which to observe events. For example, "myBucket" or "projects/my-project/topics/my-topic". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#resource CloudfunctionsFunction#resource}
        :param failure_policy: failure_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#failure_policy CloudfunctionsFunction#failure_policy}
        '''
        if isinstance(failure_policy, dict):
            failure_policy = CloudfunctionsFunctionEventTriggerFailurePolicy(**failure_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2f0f96016a1693af196f3172a858a0a80a615da1e8fb355cf170bb6add7f69)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#event_type CloudfunctionsFunction#event_type}
        '''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(self) -> builtins.str:
        '''The name or partial URI of the resource from which to observe events. For example, "myBucket" or "projects/my-project/topics/my-topic".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#resource CloudfunctionsFunction#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_policy(
        self,
    ) -> typing.Optional["CloudfunctionsFunctionEventTriggerFailurePolicy"]:
        '''failure_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#failure_policy CloudfunctionsFunction#failure_policy}
        '''
        result = self._values.get("failure_policy")
        return typing.cast(typing.Optional["CloudfunctionsFunctionEventTriggerFailurePolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionEventTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionEventTriggerFailurePolicy",
    jsii_struct_bases=[],
    name_mapping={"retry": "retry"},
)
class CloudfunctionsFunctionEventTriggerFailurePolicy:
    def __init__(
        self,
        *,
        retry: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param retry: Whether the function should be retried on failure. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#retry CloudfunctionsFunction#retry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc53281b70c6b1b58dd0992578781822573f0d8b3cf8ad54f9f1593ec5cf2e2)
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retry": retry,
        }

    @builtins.property
    def retry(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the function should be retried on failure. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#retry CloudfunctionsFunction#retry}
        '''
        result = self._values.get("retry")
        assert result is not None, "Required property 'retry' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionEventTriggerFailurePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfunctionsFunctionEventTriggerFailurePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionEventTriggerFailurePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fcda43c24269386c6bacb147fc4aeee7a9c25345393d5615d3d7f3263a36abe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d258617788c1998838b4ed3981fc9ee3647e9db12f4bcc55713fb6a9d947a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfunctionsFunctionEventTriggerFailurePolicy]:
        return typing.cast(typing.Optional[CloudfunctionsFunctionEventTriggerFailurePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfunctionsFunctionEventTriggerFailurePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805c5ceee44a01f5182b5de0ce8839db05a8485d7fafe9bdad4b074396b74248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfunctionsFunctionEventTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionEventTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aaeaab64c5ec5d2cf6f5e8d8bfa904b0692e0bdf30265e73606bbdf927160e3)
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
        :param retry: Whether the function should be retried on failure. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#retry CloudfunctionsFunction#retry}
        '''
        value = CloudfunctionsFunctionEventTriggerFailurePolicy(retry=retry)

        return typing.cast(None, jsii.invoke(self, "putFailurePolicy", [value]))

    @jsii.member(jsii_name="resetFailurePolicy")
    def reset_failure_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailurePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="failurePolicy")
    def failure_policy(
        self,
    ) -> CloudfunctionsFunctionEventTriggerFailurePolicyOutputReference:
        return typing.cast(CloudfunctionsFunctionEventTriggerFailurePolicyOutputReference, jsii.get(self, "failurePolicy"))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="failurePolicyInput")
    def failure_policy_input(
        self,
    ) -> typing.Optional[CloudfunctionsFunctionEventTriggerFailurePolicy]:
        return typing.cast(typing.Optional[CloudfunctionsFunctionEventTriggerFailurePolicy], jsii.get(self, "failurePolicyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dced6187da6e7995ca259aab5820273efac47138240708bdde377be1f71ca37f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ef5656e69438ce583ce8653d2decf0fbe4b6b6398bdbdc8a2ab5a727c201cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudfunctionsFunctionEventTrigger]:
        return typing.cast(typing.Optional[CloudfunctionsFunctionEventTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfunctionsFunctionEventTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7271d7822f62c81cf2598f46f3ca74cdd3f6d0abc7063244d2300e8da8b70f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretEnvironmentVariables",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "secret": "secret",
        "version": "version",
        "project_id": "projectId",
    },
)
class CloudfunctionsFunctionSecretEnvironmentVariables:
    def __init__(
        self,
        *,
        key: builtins.str,
        secret: builtins.str,
        version: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Name of the environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#key CloudfunctionsFunction#key}
        :param secret: ID of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret CloudfunctionsFunction#secret}
        :param version: Version of the secret (version number or the string "latest"). It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new clones start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#version CloudfunctionsFunction#version}
        :param project_id: Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret. If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#project_id CloudfunctionsFunction#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9024a3c826765c2139e345f39afec1ef0ce1030fc331086f8b931eb3692ce878)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#key CloudfunctionsFunction#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''ID of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret CloudfunctionsFunction#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string "latest").

        It is recommended to use a numeric version for secret environment variables as any updates to the secret value is not reflected until new clones start.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#version CloudfunctionsFunction#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret.

        If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#project_id CloudfunctionsFunction#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionSecretEnvironmentVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfunctionsFunctionSecretEnvironmentVariablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretEnvironmentVariablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89b33b799bdf2d83252f376b5b06ba9e57ea67d196388d120f7078d5c8dfdbc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfunctionsFunctionSecretEnvironmentVariablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c3a45997403e0403e88db401fc54d11befcb57a0348a74924621a09cfede6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfunctionsFunctionSecretEnvironmentVariablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2989cfbbdfd601b98489c74b9d1a707954f62b5a1833902b1b49e7a86a74fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd4cc975ed09b607e214bb3fac585931fcd770aa983579d8c717fa0e9d1272e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b0a8eb8b7c375df7c880a62b785d2f4bd4c71393f28bf121f9684adb4c0d79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretEnvironmentVariables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretEnvironmentVariables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretEnvironmentVariables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ea78d03c06c3f187c8d7160a9bee700f469717989432fb7d94250892ee781b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfunctionsFunctionSecretEnvironmentVariablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretEnvironmentVariablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b3231716c02adb56393453a6163e853dfbcefefcf3ff43a6972be56818bde27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8b286c757121ce92e84e5f743de8d02b3a3dec7c9795766ff44baa75d1a880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17c0df3bbc0787d7c3a92c9e40a5f61be2d96f297a1e62e958f59ea0084f2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9306e58fdb87e5922f33d51b61b80e0f93c74f70895a413195f2e160f965ca01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa1f93211d462f50ddd4b24aaf22eaa5d0617ed21fde8ae02d9b65ea5ca31e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretEnvironmentVariables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretEnvironmentVariables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretEnvironmentVariables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd2dac4ed392ef93fb4cc02f22300acbff866c49332f2bfac4b7d49893a9f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "mount_path": "mountPath",
        "secret": "secret",
        "project_id": "projectId",
        "versions": "versions",
    },
)
class CloudfunctionsFunctionSecretVolumes:
    def __init__(
        self,
        *,
        mount_path: builtins.str,
        secret: builtins.str,
        project_id: typing.Optional[builtins.str] = None,
        versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mount_path: The path within the container to mount the secret volume. For example, setting the mount_path as "/etc/secrets" would mount the secret value files under the "/etc/secrets" directory. This directory will also be completely shadowed and unavailable to mount any other secrets. Recommended mount paths: "/etc/secrets" Restricted mount paths: "/cloudsql", "/dev/log", "/pod", "/proc", "/var/log". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#mount_path CloudfunctionsFunction#mount_path}
        :param secret: ID of the secret in secret manager (not the full resource name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret CloudfunctionsFunction#secret}
        :param project_id: Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret. If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#project_id CloudfunctionsFunction#project_id}
        :param versions: versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#versions CloudfunctionsFunction#versions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d63b74911a0dbce89a1e72aa64e4ae5d3ca6cc732c766c19ae25a41b92e23bd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#mount_path CloudfunctionsFunction#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> builtins.str:
        '''ID of the secret in secret manager (not the full resource name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#secret CloudfunctionsFunction#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Project identifier (due to a known limitation, only project number is supported by this field) of the project that contains the secret.

        If not set, it will be populated with the function's project, assuming that the secret exists in the same project as of the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#project_id CloudfunctionsFunction#project_id}
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def versions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumesVersions"]]]:
        '''versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#versions CloudfunctionsFunction#versions}
        '''
        result = self._values.get("versions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumesVersions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionSecretVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfunctionsFunctionSecretVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e926897dc6c67e1994ab1bc38bc4429977131c1690927791dd9d9d93a4cdeca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfunctionsFunctionSecretVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b3c77b34d47d31e25f4974e37251db9207bc9290510bf233f3121946dca5f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfunctionsFunctionSecretVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2141abab0a3b0ceb35111c6249082dfa3d67c2492c1e05a3c700e889989a6691)
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
            type_hints = typing.get_type_hints(_typecheckingstub__261aa7b29dd4ff9ca5089ac018fc8e92dcbf521dc3f63d8ebbe368d77890bb22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf48797f307b5262d05acb82a79aa239fc59b44e33af43ac091cbb272fb8942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7834ca3b1aa34e69f7a1a75b94ef3b136933b08b62542f3ce3c129ee93a53b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfunctionsFunctionSecretVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d05590e782757c0bd113b288fdb6b4c519946fc14cb04dce1c98b73fd5b4d303)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVersions")
    def put_versions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfunctionsFunctionSecretVolumesVersions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf141d9dfdcd63dd303ca09261ae86c62731dda663279a712e8e7c0953ca6a57)
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
    def versions(self) -> "CloudfunctionsFunctionSecretVolumesVersionsList":
        return typing.cast("CloudfunctionsFunctionSecretVolumesVersionsList", jsii.get(self, "versions"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumesVersions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfunctionsFunctionSecretVolumesVersions"]]], jsii.get(self, "versionsInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72303bb92b8772a43f2604b98ae102b6885a447f24e63de1224983b4506f576b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74257da63461b849c3a2ba283e04d365ba4d4ed7687a3ec35329f95b567f256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb70e607fed9a875162f6736bdf3c806daee6766be044185f80d351781df783d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be018d17bc9e9e8f667aa7183c5373c63015eadc0d58e1a3968dfee6f20c92e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretVolumesVersions",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "version": "version"},
)
class CloudfunctionsFunctionSecretVolumesVersions:
    def __init__(self, *, path: builtins.str, version: builtins.str) -> None:
        '''
        :param path: Relative path of the file under the mount path where the secret value for this version will be fetched and made available. For example, setting the mount_path as "/etc/secrets" and path as "/secret_foo" would mount the secret value file at "/etc/secrets/secret_foo". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#path CloudfunctionsFunction#path}
        :param version: Version of the secret (version number or the string "latest"). It is preferable to use "latest" version with secret volumes as secret value changes are reflected immediately. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#version CloudfunctionsFunction#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d35a363e5a3523554380de5ea724000c346b603cfedc447c1c73750cc83b6c6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#path CloudfunctionsFunction#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Version of the secret (version number or the string "latest").

        It is preferable to use "latest" version with secret volumes as secret value changes are reflected immediately.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#version CloudfunctionsFunction#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionSecretVolumesVersions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfunctionsFunctionSecretVolumesVersionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretVolumesVersionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50e4ebbd0370ee60cfb797df0c7b3de41da757584d421a55768e6ab4b2d0d2ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfunctionsFunctionSecretVolumesVersionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2274f13aebbb7712fe09a11d1fe732602a3fa3dcb14b842856e2f8dff7d86458)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfunctionsFunctionSecretVolumesVersionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569ae8a324ac3e41c9ee503d077f5322c5ab4a458e210b81fbdec0d6779706de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cef4dff661fcaa5f2b65fc33e8db312d997d580e0e4e66097b69b3d69ba1b9e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7d471a849a2ef36b3db4d16bd6d5158a8f12648dd7487d41284e60475993e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumesVersions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumesVersions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumesVersions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ae4e0833692aff7a59a141726f604b6940cba927030140ac26b7455c0827db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfunctionsFunctionSecretVolumesVersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSecretVolumesVersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8990872bd10525daef5bb74faddb5b218ac3a5bc86d3dee82737b672f718830)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3f5d1d4a3860f22e71b3fa620f77441c57bd4b585debdc12374f0d8114cb59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd976df290b236efa68062ff30a310cf8ffff5a220963dfb4950fdd9e17cc0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumesVersions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumesVersions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumesVersions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8660af5d6f8fa0f1a779cfd70606a466590765c772fcf8e85fa67fd7a09c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSourceRepository",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class CloudfunctionsFunctionSourceRepository:
    def __init__(self, *, url: builtins.str) -> None:
        '''
        :param url: The URL pointing to the hosted repository where the function is defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#url CloudfunctionsFunction#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2dc3ed79edd40c7fa7a6a0daf34461a8c5e74bc03120d27e3db7416722d7b5)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL pointing to the hosted repository where the function is defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#url CloudfunctionsFunction#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionSourceRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfunctionsFunctionSourceRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionSourceRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efe5d0d285973ed1c27978ea7aac1ad4f6749711d0e7ef15175b4bd867a5cbd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__182013a26680eab33060ca343717a4028f2eb9d24e4ee1aed0dcc962e0446170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudfunctionsFunctionSourceRepository]:
        return typing.cast(typing.Optional[CloudfunctionsFunctionSourceRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfunctionsFunctionSourceRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fb56cac73cfa3534bb3efd7304332b0058b2e203eeb777b428cd1afea95fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CloudfunctionsFunctionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#create CloudfunctionsFunction#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#delete CloudfunctionsFunction#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#read CloudfunctionsFunction#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#update CloudfunctionsFunction#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c800dfff1a7d1324be878d22f86ec49f7edf929f8357cedb68d9242033801b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#create CloudfunctionsFunction#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#delete CloudfunctionsFunction#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#read CloudfunctionsFunction#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloudfunctions_function#update CloudfunctionsFunction#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfunctionsFunctionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfunctionsFunctionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudfunctionsFunction.CloudfunctionsFunctionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b6bdd5dc013ec3479e7e76c22ff347de4bf93b7822c9062281ebc49dde9c276)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4fefdb22d6b32c42ab02d0fa9308dee8d143325ad34c9a92175b42b6a5a669f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48dd56532b96e7a0ef74950c9261209229f49c3a49b2483b1b9cb75b0567958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2ff62836b7cb0972cbe1ae3bd3f85eb0b2760e97bbc2b51ba13b0c10234670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f86c82882ca90babc56d86c4da558e439c5999d0d5e52b6d2a89f9691bd950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9435a3583d3193a0252d2c828904dc28bcd4c9e7a9dd203a2820d2ab8103374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudfunctionsFunction",
    "CloudfunctionsFunctionConfig",
    "CloudfunctionsFunctionEventTrigger",
    "CloudfunctionsFunctionEventTriggerFailurePolicy",
    "CloudfunctionsFunctionEventTriggerFailurePolicyOutputReference",
    "CloudfunctionsFunctionEventTriggerOutputReference",
    "CloudfunctionsFunctionSecretEnvironmentVariables",
    "CloudfunctionsFunctionSecretEnvironmentVariablesList",
    "CloudfunctionsFunctionSecretEnvironmentVariablesOutputReference",
    "CloudfunctionsFunctionSecretVolumes",
    "CloudfunctionsFunctionSecretVolumesList",
    "CloudfunctionsFunctionSecretVolumesOutputReference",
    "CloudfunctionsFunctionSecretVolumesVersions",
    "CloudfunctionsFunctionSecretVolumesVersionsList",
    "CloudfunctionsFunctionSecretVolumesVersionsOutputReference",
    "CloudfunctionsFunctionSourceRepository",
    "CloudfunctionsFunctionSourceRepositoryOutputReference",
    "CloudfunctionsFunctionTimeouts",
    "CloudfunctionsFunctionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0a89ecd4c85b9f139b8aa86d6db733fc68643fd1ba20f9fed4cced0a019867d2(
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
    event_trigger: typing.Optional[typing.Union[CloudfunctionsFunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
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
    secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    source_archive_bucket: typing.Optional[builtins.str] = None,
    source_archive_object: typing.Optional[builtins.str] = None,
    source_repository: typing.Optional[typing.Union[CloudfunctionsFunctionSourceRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CloudfunctionsFunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0433b725b3bb85308b11cb46ad410115d690a34d86d338d616ab4c7aeb6dd6a2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cfe612170de2240536f6c63fddb0ffe95335f4b8a69b35c5734a719b321ac5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3a49df0dfed6908175e29739658509f97c119c2579a4cf7a2314af7943369f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0032effa2dca76f1475fede909fbe1687c873574ad902418945e9e1cca21d662(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74baee3f9f62407776543ef761c0049263caa5bb61ec4ee6b3689be24d696144(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93965384f07f6de63774cf3baa6779a8eea3fcb375eebb0e3f3fd6c78b56e766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a853b4325513d67681dca7f9a5c86fe1073f62f494e10bdfa56a4b326ef8e78b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b6b2035a9c2fc73952fd4020edebac36bd8f2685316f37b263edd02d303a9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9299a352e7764b5a79723885756a2a82504d87b5b0e3da4be8e6e55a15936861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e43e2c211fc4068574c7cc4b1c9509356d4ccb1f6b466da27f4e29274e5ced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627aace216a71caf3f59b45a35d0bd560371dd2d75947d56a54a12b7207f523a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e99dec82bc16241ae4e139ee604bcdd3de4b82c9437aed42fe3b37ba05708a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb17d89266a116318ea9bf7f7f6d6cde546c695ae99c6482448b567a59fc893e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c14a7f5a2fdf2d75e51d8c78f3a035fa46eddd2852d8baab77c5636a0f216c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7520e3b0364fb6476d9584147c240b165b6e7cb2b9eac70e817167e82157c568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0459e47c574c6008b0da3225d48ad0d92452d59034460e31dc44897b6431c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d942088928fd6a3949ff4c930eb268cd58fc74f4df04c365c876cceb57d21f4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74677ce7e89ac4c038b5b29ed9dffb0dc9997cd0aa0daabbd9d7e44957cc202(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6cd1de3aa9b75529340c8e257c437f79be3563f45e170311866b6d1a0f3b59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30623a7297a659a2cc9c79211d9f4b962ad3ed6c42d6a0edf05b175d86461279(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1e07dd3f3a59bc57aa882d28589a311ea22c11b9b6873a103d7ef0d92e68e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e91718ed43fe495b52c15b4b89721a5a6a5c3be0487cb670928aa2f502eb62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc773c3cf635ce86acdcf7ecd5be7fdb562b2a0ffcdd6f042cc1a37eb245e330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e721c991a487d7fcfcbac469882f6833a584c73dd2799689162fdb1f1b6970f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c897f8c651b389e687c7da7aca5c05723540a879fc95b2e618c7191a23fb56e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8875ac83a3b4369daeaf3d3bea06a1becff3b8e1bcd90d6df81e9e98effe29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293561b179a5288767701ddb3908f7f8e3f787cd9f1e43f19f53fe8252026475(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5996631f71c287a90f5e518154adf0d243272ede0afec36403f2b232b7b0eb9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b71a5ce18f08b7cfc2583dfff1b05a21fe12b5535c3321ae5f3a6e2251d42a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eb0f40ff668a0d603d76dd0be0ff9b5d5c77b7ca0a0ca43a6910ab7e167da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a506147f50af40675a444b8fdd52d9c93616ec83cc44d5ad4a633294bd58331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4631a97f603e2728b49d8c2d5949bfc3d7cd5d63fd513639b81a9c1aa306429(
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
    event_trigger: typing.Optional[typing.Union[CloudfunctionsFunctionEventTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
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
    secret_environment_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretEnvironmentVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    secret_volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account_email: typing.Optional[builtins.str] = None,
    source_archive_bucket: typing.Optional[builtins.str] = None,
    source_archive_object: typing.Optional[builtins.str] = None,
    source_repository: typing.Optional[typing.Union[CloudfunctionsFunctionSourceRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[CloudfunctionsFunctionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trigger_http: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vpc_connector: typing.Optional[builtins.str] = None,
    vpc_connector_egress_settings: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2f0f96016a1693af196f3172a858a0a80a615da1e8fb355cf170bb6add7f69(
    *,
    event_type: builtins.str,
    resource: builtins.str,
    failure_policy: typing.Optional[typing.Union[CloudfunctionsFunctionEventTriggerFailurePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc53281b70c6b1b58dd0992578781822573f0d8b3cf8ad54f9f1593ec5cf2e2(
    *,
    retry: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fcda43c24269386c6bacb147fc4aeee7a9c25345393d5615d3d7f3263a36abe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d258617788c1998838b4ed3981fc9ee3647e9db12f4bcc55713fb6a9d947a87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805c5ceee44a01f5182b5de0ce8839db05a8485d7fafe9bdad4b074396b74248(
    value: typing.Optional[CloudfunctionsFunctionEventTriggerFailurePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aaeaab64c5ec5d2cf6f5e8d8bfa904b0692e0bdf30265e73606bbdf927160e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dced6187da6e7995ca259aab5820273efac47138240708bdde377be1f71ca37f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ef5656e69438ce583ce8653d2decf0fbe4b6b6398bdbdc8a2ab5a727c201cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7271d7822f62c81cf2598f46f3ca74cdd3f6d0abc7063244d2300e8da8b70f2f(
    value: typing.Optional[CloudfunctionsFunctionEventTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9024a3c826765c2139e345f39afec1ef0ce1030fc331086f8b931eb3692ce878(
    *,
    key: builtins.str,
    secret: builtins.str,
    version: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b33b799bdf2d83252f376b5b06ba9e57ea67d196388d120f7078d5c8dfdbc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c3a45997403e0403e88db401fc54d11befcb57a0348a74924621a09cfede6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2989cfbbdfd601b98489c74b9d1a707954f62b5a1833902b1b49e7a86a74fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4cc975ed09b607e214bb3fac585931fcd770aa983579d8c717fa0e9d1272e2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0a8eb8b7c375df7c880a62b785d2f4bd4c71393f28bf121f9684adb4c0d79a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ea78d03c06c3f187c8d7160a9bee700f469717989432fb7d94250892ee781b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretEnvironmentVariables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3231716c02adb56393453a6163e853dfbcefefcf3ff43a6972be56818bde27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8b286c757121ce92e84e5f743de8d02b3a3dec7c9795766ff44baa75d1a880(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17c0df3bbc0787d7c3a92c9e40a5f61be2d96f297a1e62e958f59ea0084f2ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9306e58fdb87e5922f33d51b61b80e0f93c74f70895a413195f2e160f965ca01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa1f93211d462f50ddd4b24aaf22eaa5d0617ed21fde8ae02d9b65ea5ca31e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd2dac4ed392ef93fb4cc02f22300acbff866c49332f2bfac4b7d49893a9f27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretEnvironmentVariables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d63b74911a0dbce89a1e72aa64e4ae5d3ca6cc732c766c19ae25a41b92e23bd(
    *,
    mount_path: builtins.str,
    secret: builtins.str,
    project_id: typing.Optional[builtins.str] = None,
    versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e926897dc6c67e1994ab1bc38bc4429977131c1690927791dd9d9d93a4cdeca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b3c77b34d47d31e25f4974e37251db9207bc9290510bf233f3121946dca5f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2141abab0a3b0ceb35111c6249082dfa3d67c2492c1e05a3c700e889989a6691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261aa7b29dd4ff9ca5089ac018fc8e92dcbf521dc3f63d8ebbe368d77890bb22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf48797f307b5262d05acb82a79aa239fc59b44e33af43ac091cbb272fb8942(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7834ca3b1aa34e69f7a1a75b94ef3b136933b08b62542f3ce3c129ee93a53b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05590e782757c0bd113b288fdb6b4c519946fc14cb04dce1c98b73fd5b4d303(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf141d9dfdcd63dd303ca09261ae86c62731dda663279a712e8e7c0953ca6a57(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfunctionsFunctionSecretVolumesVersions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72303bb92b8772a43f2604b98ae102b6885a447f24e63de1224983b4506f576b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74257da63461b849c3a2ba283e04d365ba4d4ed7687a3ec35329f95b567f256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb70e607fed9a875162f6736bdf3c806daee6766be044185f80d351781df783d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be018d17bc9e9e8f667aa7183c5373c63015eadc0d58e1a3968dfee6f20c92e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d35a363e5a3523554380de5ea724000c346b603cfedc447c1c73750cc83b6c6(
    *,
    path: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e4ebbd0370ee60cfb797df0c7b3de41da757584d421a55768e6ab4b2d0d2ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2274f13aebbb7712fe09a11d1fe732602a3fa3dcb14b842856e2f8dff7d86458(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569ae8a324ac3e41c9ee503d077f5322c5ab4a458e210b81fbdec0d6779706de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef4dff661fcaa5f2b65fc33e8db312d997d580e0e4e66097b69b3d69ba1b9e1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d471a849a2ef36b3db4d16bd6d5158a8f12648dd7487d41284e60475993e6e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ae4e0833692aff7a59a141726f604b6940cba927030140ac26b7455c0827db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfunctionsFunctionSecretVolumesVersions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8990872bd10525daef5bb74faddb5b218ac3a5bc86d3dee82737b672f718830(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f5d1d4a3860f22e71b3fa620f77441c57bd4b585debdc12374f0d8114cb59b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd976df290b236efa68062ff30a310cf8ffff5a220963dfb4950fdd9e17cc0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8660af5d6f8fa0f1a779cfd70606a466590765c772fcf8e85fa67fd7a09c27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionSecretVolumesVersions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2dc3ed79edd40c7fa7a6a0daf34461a8c5e74bc03120d27e3db7416722d7b5(
    *,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe5d0d285973ed1c27978ea7aac1ad4f6749711d0e7ef15175b4bd867a5cbd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182013a26680eab33060ca343717a4028f2eb9d24e4ee1aed0dcc962e0446170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fb56cac73cfa3534bb3efd7304332b0058b2e203eeb777b428cd1afea95fe3(
    value: typing.Optional[CloudfunctionsFunctionSourceRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c800dfff1a7d1324be878d22f86ec49f7edf929f8357cedb68d9242033801b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6bdd5dc013ec3479e7e76c22ff347de4bf93b7822c9062281ebc49dde9c276(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fefdb22d6b32c42ab02d0fa9308dee8d143325ad34c9a92175b42b6a5a669f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48dd56532b96e7a0ef74950c9261209229f49c3a49b2483b1b9cb75b0567958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2ff62836b7cb0972cbe1ae3bd3f85eb0b2760e97bbc2b51ba13b0c10234670(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f86c82882ca90babc56d86c4da558e439c5999d0d5e52b6d2a89f9691bd950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9435a3583d3193a0252d2c828904dc28bcd4c9e7a9dd203a2820d2ab8103374(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfunctionsFunctionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
