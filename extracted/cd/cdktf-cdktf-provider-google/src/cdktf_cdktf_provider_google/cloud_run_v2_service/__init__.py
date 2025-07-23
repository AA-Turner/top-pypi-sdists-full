r'''
# `google_cloud_run_v2_service`

Refer to the Terraform Registry for docs: [`google_cloud_run_v2_service`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service).
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


class CloudRunV2Service(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2Service",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service google_cloud_run_v2_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        template: typing.Union["CloudRunV2ServiceTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["CloudRunV2ServiceBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        build_config: typing.Optional[typing.Union["CloudRunV2ServiceBuildConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ingress: typing.Optional[builtins.str] = None,
        invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["CloudRunV2ServiceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudRunV2ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service google_cloud_run_v2_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the cloud run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#location CloudRunV2Service#location}
        :param name: Name of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#template CloudRunV2Service#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources. All system annotations in v1 now have a corresponding field in v2 Service. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#annotations CloudRunV2Service#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#binary_authorization CloudRunV2Service#binary_authorization}
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#build_config CloudRunV2Service#build_config}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#client CloudRunV2Service#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#client_version CloudRunV2Service#client_version}
        :param custom_audiences: One or more custom audiences that you want this service to support. Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests. For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#custom_audiences CloudRunV2Service#custom_audiences}
        :param deletion_protection: Whether Terraform will be prevented from destroying the service. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the service, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the service will fail. When the field is set to false, deleting the service is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#deletion_protection CloudRunV2Service#deletion_protection}
        :param description: User-provided description of the Service. This field currently has a 512-character limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#description CloudRunV2Service#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#id CloudRunV2Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress: Provides the ingress settings for this Service. On output, returns the currently observed ingress settings, or INGRESS_TRAFFIC_UNSPECIFIED if no revision is active. Possible values: ["INGRESS_TRAFFIC_ALL", "INGRESS_TRAFFIC_INTERNAL_ONLY", "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#ingress CloudRunV2Service#ingress}
        :param invoker_iam_disabled: Disables IAM permission check for run.routes.invoke for callers of this service. For more information, visit https://cloud.google.com/run/docs/securing/managing-access#invoker_check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#invoker_iam_disabled CloudRunV2Service#invoker_iam_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 Service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#labels CloudRunV2Service#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#launch_stage CloudRunV2Service#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#project CloudRunV2Service#project}.
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling CloudRunV2Service#scaling}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeouts CloudRunV2Service#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#traffic CloudRunV2Service#traffic}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f648a6d9fe5b20c0bb2f5645b46ae9978684d7f9cd4b499b8f94bf209b42889)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudRunV2ServiceConfig(
            location=location,
            name=name,
            template=template,
            annotations=annotations,
            binary_authorization=binary_authorization,
            build_config=build_config,
            client=client,
            client_version=client_version,
            custom_audiences=custom_audiences,
            deletion_protection=deletion_protection,
            description=description,
            id=id,
            ingress=ingress,
            invoker_iam_disabled=invoker_iam_disabled,
            labels=labels,
            launch_stage=launch_stage,
            project=project,
            scaling=scaling,
            timeouts=timeouts,
            traffic=traffic,
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
        '''Generates CDKTF code for importing a CloudRunV2Service resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudRunV2Service to import.
        :param import_from_id: The id of the existing CloudRunV2Service that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudRunV2Service to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175ced8f1ce80e2c520e73dfd55d7418b8daa5da5480ed413835d096e1611c22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBinaryAuthorization")
    def put_binary_authorization(
        self,
        *,
        breakglass_justification: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#breakglass_justification CloudRunV2Service#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#policy CloudRunV2Service#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#use_default CloudRunV2Service#use_default}
        '''
        value = CloudRunV2ServiceBinaryAuthorization(
            breakglass_justification=breakglass_justification,
            policy=policy,
            use_default=use_default,
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putBuildConfig")
    def put_build_config(
        self,
        *,
        base_image: typing.Optional[builtins.str] = None,
        enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        function_target: typing.Optional[builtins.str] = None,
        image_uri: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_location: typing.Optional[builtins.str] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param base_image: The base image used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#base_image CloudRunV2Service#base_image}
        :param enable_automatic_updates: Sets whether the function will receive automatic base image updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#enable_automatic_updates CloudRunV2Service#enable_automatic_updates}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#environment_variables CloudRunV2Service#environment_variables}
        :param function_target: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#function_target CloudRunV2Service#function_target}
        :param image_uri: Artifact Registry URI to store the built image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#image_uri CloudRunV2Service#image_uri}
        :param service_account: Service account to be used for building the container. The format of this field is 'projects/{projectId}/serviceAccounts/{serviceAccountEmail}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service_account CloudRunV2Service#service_account}
        :param source_location: The Cloud Storage bucket URI where the function source code is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#source_location CloudRunV2Service#source_location}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the Cloud Run function. The format of this field is 'projects/{project}/locations/{region}/workerPools/{workerPool}' where {project} and {region} are the project id and region respectively where the worker pool is defined and {workerPool} is the short name of the worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#worker_pool CloudRunV2Service#worker_pool}
        '''
        value = CloudRunV2ServiceBuildConfig(
            base_image=base_image,
            enable_automatic_updates=enable_automatic_updates,
            environment_variables=environment_variables,
            function_target=function_target,
            image_uri=image_uri,
            service_account=service_account,
            source_location=source_location,
            worker_pool=worker_pool,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildConfig", [value]))

    @jsii.member(jsii_name="putScaling")
    def put_scaling(
        self,
        *,
        manual_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manual_instance_count: Total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#manual_instance_count CloudRunV2Service#manual_instance_count}
        :param min_instance_count: Minimum number of instances for the service, to be divided among all revisions receiving traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#min_instance_count CloudRunV2Service#min_instance_count}
        :param scaling_mode: The `scaling mode <https://cloud.google.com/run/docs/reference/rest/v2/projects.locations.services#scalingmode>`_ for the service. Possible values: ["AUTOMATIC", "MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling_mode CloudRunV2Service#scaling_mode}
        '''
        value = CloudRunV2ServiceScaling(
            manual_instance_count=manual_instance_count,
            min_instance_count=min_instance_count,
            scaling_mode=scaling_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putScaling", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        execution_environment: typing.Optional[builtins.str] = None,
        gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
        node_selector: typing.Optional[typing.Union["CloudRunV2ServiceTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        revision: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["CloudRunV2ServiceTemplateScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudRunV2ServiceTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 RevisionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#annotations CloudRunV2Service#annotations}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#containers CloudRunV2Service#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#encryption_key CloudRunV2Service#encryption_key}
        :param execution_environment: The sandbox environment to host this Revision. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#execution_environment CloudRunV2Service#execution_environment}
        :param gpu_zonal_redundancy_disabled: True if GPU zonal redundancy is disabled on this revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#gpu_zonal_redundancy_disabled CloudRunV2Service#gpu_zonal_redundancy_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 RevisionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#labels CloudRunV2Service#labels}
        :param max_instance_request_concurrency: Sets the maximum number of requests that each serving instance can receive. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#max_instance_request_concurrency CloudRunV2Service#max_instance_request_concurrency}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#node_selector CloudRunV2Service#node_selector}
        :param revision: The unique name for the revision. If this field is omitted, it will be automatically generated based on the Service name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#revision CloudRunV2Service#revision}
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling CloudRunV2Service#scaling}
        :param service_account: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service_account CloudRunV2Service#service_account}
        :param session_affinity: Enables session affinity. For more information, go to https://cloud.google.com/run/docs/configuring/session-affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#session_affinity CloudRunV2Service#session_affinity}
        :param timeout: Max allowed time for an instance to respond to a request. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout CloudRunV2Service#timeout}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#volumes CloudRunV2Service#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#vpc_access CloudRunV2Service#vpc_access}
        '''
        value = CloudRunV2ServiceTemplate(
            annotations=annotations,
            containers=containers,
            encryption_key=encryption_key,
            execution_environment=execution_environment,
            gpu_zonal_redundancy_disabled=gpu_zonal_redundancy_disabled,
            labels=labels,
            max_instance_request_concurrency=max_instance_request_concurrency,
            node_selector=node_selector,
            revision=revision,
            scaling=scaling,
            service_account=service_account,
            session_affinity=session_affinity,
            timeout=timeout,
            volumes=volumes,
            vpc_access=vpc_access,
        )

        return typing.cast(None, jsii.invoke(self, "putTemplate", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#create CloudRunV2Service#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#delete CloudRunV2Service#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#update CloudRunV2Service#update}.
        '''
        value = CloudRunV2ServiceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTraffic")
    def put_traffic(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTraffic", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342084dcdeb5b28d579e5f6c58cc182c3151b6cc29674e39fa2bb317a1082a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTraffic", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBinaryAuthorization")
    def reset_binary_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorization", []))

    @jsii.member(jsii_name="resetBuildConfig")
    def reset_build_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildConfig", []))

    @jsii.member(jsii_name="resetClient")
    def reset_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClient", []))

    @jsii.member(jsii_name="resetClientVersion")
    def reset_client_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientVersion", []))

    @jsii.member(jsii_name="resetCustomAudiences")
    def reset_custom_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAudiences", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIngress")
    def reset_ingress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngress", []))

    @jsii.member(jsii_name="resetInvokerIamDisabled")
    def reset_invoker_iam_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvokerIamDisabled", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLaunchStage")
    def reset_launch_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchStage", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetScaling")
    def reset_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaling", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTraffic")
    def reset_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraffic", []))

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
    @jsii.member(jsii_name="binaryAuthorization")
    def binary_authorization(
        self,
    ) -> "CloudRunV2ServiceBinaryAuthorizationOutputReference":
        return typing.cast("CloudRunV2ServiceBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="buildConfig")
    def build_config(self) -> "CloudRunV2ServiceBuildConfigOutputReference":
        return typing.cast("CloudRunV2ServiceBuildConfigOutputReference", jsii.get(self, "buildConfig"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "CloudRunV2ServiceConditionsList":
        return typing.cast("CloudRunV2ServiceConditionsList", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="creator")
    def creator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creator"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="lastModifier")
    def last_modifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifier"))

    @builtins.property
    @jsii.member(jsii_name="latestCreatedRevision")
    def latest_created_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestCreatedRevision"))

    @builtins.property
    @jsii.member(jsii_name="latestReadyRevision")
    def latest_ready_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestReadyRevision"))

    @builtins.property
    @jsii.member(jsii_name="observedGeneration")
    def observed_generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "observedGeneration"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="scaling")
    def scaling(self) -> "CloudRunV2ServiceScalingOutputReference":
        return typing.cast("CloudRunV2ServiceScalingOutputReference", jsii.get(self, "scaling"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "CloudRunV2ServiceTemplateOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="terminalCondition")
    def terminal_condition(self) -> "CloudRunV2ServiceTerminalConditionList":
        return typing.cast("CloudRunV2ServiceTerminalConditionList", jsii.get(self, "terminalCondition"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudRunV2ServiceTimeoutsOutputReference":
        return typing.cast("CloudRunV2ServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="traffic")
    def traffic(self) -> "CloudRunV2ServiceTrafficList":
        return typing.cast("CloudRunV2ServiceTrafficList", jsii.get(self, "traffic"))

    @builtins.property
    @jsii.member(jsii_name="trafficStatuses")
    def traffic_statuses(self) -> "CloudRunV2ServiceTrafficStatusesList":
        return typing.cast("CloudRunV2ServiceTrafficStatusesList", jsii.get(self, "trafficStatuses"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urls"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationInput")
    def binary_authorization_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceBinaryAuthorization"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="buildConfigInput")
    def build_config_input(self) -> typing.Optional["CloudRunV2ServiceBuildConfig"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceBuildConfig"], jsii.get(self, "buildConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="clientInput")
    def client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientInput"))

    @builtins.property
    @jsii.member(jsii_name="clientVersionInput")
    def client_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="customAudiencesInput")
    def custom_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressInput")
    def ingress_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingressInput"))

    @builtins.property
    @jsii.member(jsii_name="invokerIamDisabledInput")
    def invoker_iam_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invokerIamDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="launchStageInput")
    def launch_stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchStageInput"))

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
    @jsii.member(jsii_name="scalingInput")
    def scaling_input(self) -> typing.Optional["CloudRunV2ServiceScaling"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceScaling"], jsii.get(self, "scalingInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["CloudRunV2ServiceTemplate"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunV2ServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunV2ServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficInput")
    def traffic_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTraffic"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTraffic"]]], jsii.get(self, "trafficInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a888ebd91dccd3ef5c8c832832fe2fbf99f85f96b43ff410dabea674a4325a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "client"))

    @client.setter
    def client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36047ff638d6b5924690ddc831560c91cade2769d4e2e13641e9a4b024c4612f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "client", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientVersion")
    def client_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientVersion"))

    @client_version.setter
    def client_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b56c66002d4aaec7d99a76ebc39b64652968e45521c9e42a34f23712ad68d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customAudiences")
    def custom_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customAudiences"))

    @custom_audiences.setter
    def custom_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68fb9a0be296e7f48c40d4b23f927b7a44eab44a25d1684780d4ba2a5e3f726b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81697b62950a249967b374477b3e194593be693e9cdf5245a76035c03631a1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6767bcef21d80234e4fde68727d60f0b033791cc2869fc24bad7be256cb96209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15406630f376c4f75132ba2257f84b69f22b873269dac5a462e4254797f7f752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingress"))

    @ingress.setter
    def ingress(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0a37206e05abc3e38b9045f0014595d52b472281b61300392863afcf0cc14f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invokerIamDisabled")
    def invoker_iam_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invokerIamDisabled"))

    @invoker_iam_disabled.setter
    def invoker_iam_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa1a40fa285556246951bedf735ba2c0231d6bce4f6e44d1fc50df7aedec252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invokerIamDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c563227b75604cd3cf205483eaa37595751af7e8aa8c2d57dace8d5f634df1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchStage")
    def launch_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchStage"))

    @launch_stage.setter
    def launch_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e3d6aaed401c99c67bae47c21b430e7d068469da976cdc3fd556e00947a352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2535d080a4042b5dcb4d18d8d586d82b9ecfd6dfed78fd592417d39b132d7023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710f6012705175c08b1141341778cdd64e131b091c48ce49d82830dab9fbd1eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ebfc79cd9a40c0316f7f6d97c366e16ffb8e0f2332e4b15f5eb476d03562d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={
        "breakglass_justification": "breakglassJustification",
        "policy": "policy",
        "use_default": "useDefault",
    },
)
class CloudRunV2ServiceBinaryAuthorization:
    def __init__(
        self,
        *,
        breakglass_justification: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#breakglass_justification CloudRunV2Service#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#policy CloudRunV2Service#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#use_default CloudRunV2Service#use_default}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98bf701aa0ab33be1b50f9e63713e5f6262566a7824c223c938dce0b52351f2)
            check_type(argname="argument breakglass_justification", value=breakglass_justification, expected_type=type_hints["breakglass_justification"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument use_default", value=use_default, expected_type=type_hints["use_default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if breakglass_justification is not None:
            self._values["breakglass_justification"] = breakglass_justification
        if policy is not None:
            self._values["policy"] = policy
        if use_default is not None:
            self._values["use_default"] = use_default

    @builtins.property
    def breakglass_justification(self) -> typing.Optional[builtins.str]:
        '''If present, indicates to use Breakglass using this justification.

        If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#breakglass_justification CloudRunV2Service#breakglass_justification}
        '''
        result = self._values.get("breakglass_justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#policy CloudRunV2Service#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#use_default CloudRunV2Service#use_default}
        '''
        result = self._values.get("use_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dcbf276cb4df159682177c47892ddb850fd2ac2770c84685f520ead0381fbff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBreakglassJustification")
    def reset_breakglass_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBreakglassJustification", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @jsii.member(jsii_name="resetUseDefault")
    def reset_use_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseDefault", []))

    @builtins.property
    @jsii.member(jsii_name="breakglassJustificationInput")
    def breakglass_justification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "breakglassJustificationInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="useDefaultInput")
    def use_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="breakglassJustification")
    def breakglass_justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "breakglassJustification"))

    @breakglass_justification.setter
    def breakglass_justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50264cb8b9edf787b5117d4beb8725487c876dc03c8a2c282f6c09cf346bc56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "breakglassJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a41eaa16ce86039b4271824be584f777cadedc6e01a4ff916e4377093a35809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDefault")
    def use_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useDefault"))

    @use_default.setter
    def use_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c293f0f4b74393065b50ad1000ebb801609962195125b1028140d125acb254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceBinaryAuthorization]:
        return typing.cast(typing.Optional[CloudRunV2ServiceBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f78daabaa8266f48b310977f18ac33a83f41a7412185d3e225cd9f38e5b2f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceBuildConfig",
    jsii_struct_bases=[],
    name_mapping={
        "base_image": "baseImage",
        "enable_automatic_updates": "enableAutomaticUpdates",
        "environment_variables": "environmentVariables",
        "function_target": "functionTarget",
        "image_uri": "imageUri",
        "service_account": "serviceAccount",
        "source_location": "sourceLocation",
        "worker_pool": "workerPool",
    },
)
class CloudRunV2ServiceBuildConfig:
    def __init__(
        self,
        *,
        base_image: typing.Optional[builtins.str] = None,
        enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        function_target: typing.Optional[builtins.str] = None,
        image_uri: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_location: typing.Optional[builtins.str] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param base_image: The base image used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#base_image CloudRunV2Service#base_image}
        :param enable_automatic_updates: Sets whether the function will receive automatic base image updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#enable_automatic_updates CloudRunV2Service#enable_automatic_updates}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#environment_variables CloudRunV2Service#environment_variables}
        :param function_target: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#function_target CloudRunV2Service#function_target}
        :param image_uri: Artifact Registry URI to store the built image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#image_uri CloudRunV2Service#image_uri}
        :param service_account: Service account to be used for building the container. The format of this field is 'projects/{projectId}/serviceAccounts/{serviceAccountEmail}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service_account CloudRunV2Service#service_account}
        :param source_location: The Cloud Storage bucket URI where the function source code is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#source_location CloudRunV2Service#source_location}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the Cloud Run function. The format of this field is 'projects/{project}/locations/{region}/workerPools/{workerPool}' where {project} and {region} are the project id and region respectively where the worker pool is defined and {workerPool} is the short name of the worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#worker_pool CloudRunV2Service#worker_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f52c1114aaf4ac96ae62aa799e11605fdfa6146b957383fea9d30841279c17a)
            check_type(argname="argument base_image", value=base_image, expected_type=type_hints["base_image"])
            check_type(argname="argument enable_automatic_updates", value=enable_automatic_updates, expected_type=type_hints["enable_automatic_updates"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument function_target", value=function_target, expected_type=type_hints["function_target"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument source_location", value=source_location, expected_type=type_hints["source_location"])
            check_type(argname="argument worker_pool", value=worker_pool, expected_type=type_hints["worker_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_image is not None:
            self._values["base_image"] = base_image
        if enable_automatic_updates is not None:
            self._values["enable_automatic_updates"] = enable_automatic_updates
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if function_target is not None:
            self._values["function_target"] = function_target
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if service_account is not None:
            self._values["service_account"] = service_account
        if source_location is not None:
            self._values["source_location"] = source_location
        if worker_pool is not None:
            self._values["worker_pool"] = worker_pool

    @builtins.property
    def base_image(self) -> typing.Optional[builtins.str]:
        '''The base image used to build the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#base_image CloudRunV2Service#base_image}
        '''
        result = self._values.get("base_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_automatic_updates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Sets whether the function will receive automatic base image updates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#enable_automatic_updates CloudRunV2Service#enable_automatic_updates}
        '''
        result = self._values.get("enable_automatic_updates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-provided build-time environment variables for the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#environment_variables CloudRunV2Service#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def function_target(self) -> typing.Optional[builtins.str]:
        '''The name of the function (as defined in source code) that will be executed.

        Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#function_target CloudRunV2Service#function_target}
        '''
        result = self._values.get("function_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry URI to store the built image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#image_uri CloudRunV2Service#image_uri}
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account to be used for building the container. The format of this field is 'projects/{projectId}/serviceAccounts/{serviceAccountEmail}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service_account CloudRunV2Service#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage bucket URI where the function source code is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#source_location CloudRunV2Service#source_location}
        '''
        result = self._values.get("source_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Build Custom Worker Pool that should be used to build the Cloud Run function.

        The format of this field is 'projects/{project}/locations/{region}/workerPools/{workerPool}' where {project} and {region} are the project id and region respectively where the worker pool is defined and {workerPool} is the short name of the worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#worker_pool CloudRunV2Service#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceBuildConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceBuildConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceBuildConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5515a9e10807d68fb42905bd5d982d4f527f2272a2009c3fa668a073704f31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBaseImage")
    def reset_base_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseImage", []))

    @jsii.member(jsii_name="resetEnableAutomaticUpdates")
    def reset_enable_automatic_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAutomaticUpdates", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetFunctionTarget")
    def reset_function_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionTarget", []))

    @jsii.member(jsii_name="resetImageUri")
    def reset_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUri", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetSourceLocation")
    def reset_source_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceLocation", []))

    @jsii.member(jsii_name="resetWorkerPool")
    def reset_worker_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerPool", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="baseImageInput")
    def base_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseImageInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdatesInput")
    def enable_automatic_updates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAutomaticUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="functionTargetInput")
    def function_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceLocationInput")
    def source_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="workerPoolInput")
    def worker_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="baseImage")
    def base_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseImage"))

    @base_image.setter
    def base_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fff98a91a613aaf7ec4c285f54b857bd5b271910e1eed726797724fc60da585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdates")
    def enable_automatic_updates(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAutomaticUpdates"))

    @enable_automatic_updates.setter
    def enable_automatic_updates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1486d6aff57c6ae853b4f444c0aed017ac5a60dd82264594d46e7961e31ef917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutomaticUpdates", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__7b97f58b9ce4d0412c43501d546782c3a9787a8c2ce8478d294fcd5597e39e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionTarget")
    def function_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionTarget"))

    @function_target.setter
    def function_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff7775364b3f8228d27ac3175f01c9f55c04a23159f4687239a4332b33539a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3e0ca4f341a96b053fd0ba8a240aeb6fad67ede21bcdba14a64025963bc5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f0d4e19f4ba214943ebfaf8e43097829222953f20260449b668d5078d56fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceLocation")
    def source_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceLocation"))

    @source_location.setter
    def source_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b38c077d279539164c76448b30de0f3f6189ba3e83dac3da4dbc9e0e9fcd91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c908890d70d8e11ee420239850a7771e9ff73c9ddec3ba00917b393eb381c5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceBuildConfig]:
        return typing.cast(typing.Optional[CloudRunV2ServiceBuildConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceBuildConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a9a477090be0cd89d63cfaaf0ea164fa535c1ac49bfb3984fdc640d6a515db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2ServiceConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d2c410b6b5e91f359844872e2d53e132bac5003f9ddcbbd5a3bee1131d3f77e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudRunV2ServiceConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53217eb0573812a99323f60f5e7f83dba2bdd9f010ac41d14ac374da9f55007)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c138c8a4c0aaf23a80da766270066b921f69f71f57bd2d944864dc5b93d1ab86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9f1061a1758860c9ad8d47911cf33c840263c294a03faff97ff1155fc684260)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1069e7b106044e36d1d3f375f2703e5887c60b085353263790de3277bd25bd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caa62713a40a8a2e5483ade04e5ee98e1d1403827d00e01ad9335f5210050a8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="executionReason")
    def execution_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionReason"))

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="revisionReason")
    def revision_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionReason"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceConditions]:
        return typing.cast(typing.Optional[CloudRunV2ServiceConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f8a263326f798303080419fe029a2dd97dea09f2403280c346b4e8e7bbacf6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceConfig",
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
        "template": "template",
        "annotations": "annotations",
        "binary_authorization": "binaryAuthorization",
        "build_config": "buildConfig",
        "client": "client",
        "client_version": "clientVersion",
        "custom_audiences": "customAudiences",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "id": "id",
        "ingress": "ingress",
        "invoker_iam_disabled": "invokerIamDisabled",
        "labels": "labels",
        "launch_stage": "launchStage",
        "project": "project",
        "scaling": "scaling",
        "timeouts": "timeouts",
        "traffic": "traffic",
    },
)
class CloudRunV2ServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        template: typing.Union["CloudRunV2ServiceTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[CloudRunV2ServiceBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        build_config: typing.Optional[typing.Union[CloudRunV2ServiceBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ingress: typing.Optional[builtins.str] = None,
        invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["CloudRunV2ServiceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudRunV2ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the cloud run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#location CloudRunV2Service#location}
        :param name: Name of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#template CloudRunV2Service#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources. All system annotations in v1 now have a corresponding field in v2 Service. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#annotations CloudRunV2Service#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#binary_authorization CloudRunV2Service#binary_authorization}
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#build_config CloudRunV2Service#build_config}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#client CloudRunV2Service#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#client_version CloudRunV2Service#client_version}
        :param custom_audiences: One or more custom audiences that you want this service to support. Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests. For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#custom_audiences CloudRunV2Service#custom_audiences}
        :param deletion_protection: Whether Terraform will be prevented from destroying the service. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the service, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the service will fail. When the field is set to false, deleting the service is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#deletion_protection CloudRunV2Service#deletion_protection}
        :param description: User-provided description of the Service. This field currently has a 512-character limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#description CloudRunV2Service#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#id CloudRunV2Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress: Provides the ingress settings for this Service. On output, returns the currently observed ingress settings, or INGRESS_TRAFFIC_UNSPECIFIED if no revision is active. Possible values: ["INGRESS_TRAFFIC_ALL", "INGRESS_TRAFFIC_INTERNAL_ONLY", "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#ingress CloudRunV2Service#ingress}
        :param invoker_iam_disabled: Disables IAM permission check for run.routes.invoke for callers of this service. For more information, visit https://cloud.google.com/run/docs/securing/managing-access#invoker_check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#invoker_iam_disabled CloudRunV2Service#invoker_iam_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 Service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#labels CloudRunV2Service#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#launch_stage CloudRunV2Service#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#project CloudRunV2Service#project}.
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling CloudRunV2Service#scaling}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeouts CloudRunV2Service#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#traffic CloudRunV2Service#traffic}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(template, dict):
            template = CloudRunV2ServiceTemplate(**template)
        if isinstance(binary_authorization, dict):
            binary_authorization = CloudRunV2ServiceBinaryAuthorization(**binary_authorization)
        if isinstance(build_config, dict):
            build_config = CloudRunV2ServiceBuildConfig(**build_config)
        if isinstance(scaling, dict):
            scaling = CloudRunV2ServiceScaling(**scaling)
        if isinstance(timeouts, dict):
            timeouts = CloudRunV2ServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0014b5e160c040f73cda4019aa150a8fc78aef2b68cfeda3ed6a8efcc1b071f0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument binary_authorization", value=binary_authorization, expected_type=type_hints["binary_authorization"])
            check_type(argname="argument build_config", value=build_config, expected_type=type_hints["build_config"])
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument client_version", value=client_version, expected_type=type_hints["client_version"])
            check_type(argname="argument custom_audiences", value=custom_audiences, expected_type=type_hints["custom_audiences"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingress", value=ingress, expected_type=type_hints["ingress"])
            check_type(argname="argument invoker_iam_disabled", value=invoker_iam_disabled, expected_type=type_hints["invoker_iam_disabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launch_stage", value=launch_stage, expected_type=type_hints["launch_stage"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "template": template,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if binary_authorization is not None:
            self._values["binary_authorization"] = binary_authorization
        if build_config is not None:
            self._values["build_config"] = build_config
        if client is not None:
            self._values["client"] = client
        if client_version is not None:
            self._values["client_version"] = client_version
        if custom_audiences is not None:
            self._values["custom_audiences"] = custom_audiences
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ingress is not None:
            self._values["ingress"] = ingress
        if invoker_iam_disabled is not None:
            self._values["invoker_iam_disabled"] = invoker_iam_disabled
        if labels is not None:
            self._values["labels"] = labels
        if launch_stage is not None:
            self._values["launch_stage"] = launch_stage
        if project is not None:
            self._values["project"] = project
        if scaling is not None:
            self._values["scaling"] = scaling
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if traffic is not None:
            self._values["traffic"] = traffic

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
        '''The location of the cloud run service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#location CloudRunV2Service#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "CloudRunV2ServiceTemplate":
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#template CloudRunV2Service#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("CloudRunV2ServiceTemplate", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that may be set by external tools to store and arbitrary metadata.

        They are not queryable and should be preserved when modifying objects.

        Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources.
        All system annotations in v1 now have a corresponding field in v2 Service.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#annotations CloudRunV2Service#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[CloudRunV2ServiceBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#binary_authorization CloudRunV2Service#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[CloudRunV2ServiceBinaryAuthorization], result)

    @builtins.property
    def build_config(self) -> typing.Optional[CloudRunV2ServiceBuildConfig]:
        '''build_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#build_config CloudRunV2Service#build_config}
        '''
        result = self._values.get("build_config")
        return typing.cast(typing.Optional[CloudRunV2ServiceBuildConfig], result)

    @builtins.property
    def client(self) -> typing.Optional[builtins.str]:
        '''Arbitrary identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#client CloudRunV2Service#client}
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_version(self) -> typing.Optional[builtins.str]:
        '''Arbitrary version identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#client_version CloudRunV2Service#client_version}
        '''
        result = self._values.get("client_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more custom audiences that you want this service to support.

        Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests.
        For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#custom_audiences CloudRunV2Service#custom_audiences}
        '''
        result = self._values.get("custom_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the service.

        Defaults to true.
        When a'terraform destroy' or 'terraform apply' would delete the service,
        the command will fail if this field is not set to false in Terraform state.
        When the field is set to true or unset in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the service will fail.
        When the field is set to false, deleting the service is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#deletion_protection CloudRunV2Service#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description of the Service. This field currently has a 512-character limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#description CloudRunV2Service#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#id CloudRunV2Service#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress(self) -> typing.Optional[builtins.str]:
        '''Provides the ingress settings for this Service.

        On output, returns the currently observed ingress settings, or INGRESS_TRAFFIC_UNSPECIFIED if no revision is active. Possible values: ["INGRESS_TRAFFIC_ALL", "INGRESS_TRAFFIC_INTERNAL_ONLY", "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#ingress CloudRunV2Service#ingress}
        '''
        result = self._values.get("ingress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invoker_iam_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables IAM permission check for run.routes.invoke for callers of this service. For more information, visit https://cloud.google.com/run/docs/securing/managing-access#invoker_check.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#invoker_iam_disabled CloudRunV2Service#invoker_iam_disabled}
        '''
        result = self._values.get("invoker_iam_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component,
        environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with  'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 Service.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#labels CloudRunV2Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def launch_stage(self) -> typing.Optional[builtins.str]:
        '''The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features.

        For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#launch_stage CloudRunV2Service#launch_stage}
        '''
        result = self._values.get("launch_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#project CloudRunV2Service#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling(self) -> typing.Optional["CloudRunV2ServiceScaling"]:
        '''scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling CloudRunV2Service#scaling}
        '''
        result = self._values.get("scaling")
        return typing.cast(typing.Optional["CloudRunV2ServiceScaling"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudRunV2ServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeouts CloudRunV2Service#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudRunV2ServiceTimeouts"], result)

    @builtins.property
    def traffic(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTraffic"]]]:
        '''traffic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#traffic CloudRunV2Service#traffic}
        '''
        result = self._values.get("traffic")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTraffic"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceScaling",
    jsii_struct_bases=[],
    name_mapping={
        "manual_instance_count": "manualInstanceCount",
        "min_instance_count": "minInstanceCount",
        "scaling_mode": "scalingMode",
    },
)
class CloudRunV2ServiceScaling:
    def __init__(
        self,
        *,
        manual_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manual_instance_count: Total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#manual_instance_count CloudRunV2Service#manual_instance_count}
        :param min_instance_count: Minimum number of instances for the service, to be divided among all revisions receiving traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#min_instance_count CloudRunV2Service#min_instance_count}
        :param scaling_mode: The `scaling mode <https://cloud.google.com/run/docs/reference/rest/v2/projects.locations.services#scalingmode>`_ for the service. Possible values: ["AUTOMATIC", "MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling_mode CloudRunV2Service#scaling_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c7a86c3f9c282ed6076748a69464579370f6bbbba04519875d2d00fc68fd23)
            check_type(argname="argument manual_instance_count", value=manual_instance_count, expected_type=type_hints["manual_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument scaling_mode", value=scaling_mode, expected_type=type_hints["scaling_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manual_instance_count is not None:
            self._values["manual_instance_count"] = manual_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if scaling_mode is not None:
            self._values["scaling_mode"] = scaling_mode

    @builtins.property
    def manual_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Total instance count for the service in manual scaling mode.

        This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#manual_instance_count CloudRunV2Service#manual_instance_count}
        '''
        result = self._values.get("manual_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of instances for the service, to be divided among all revisions receiving traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#min_instance_count CloudRunV2Service#min_instance_count}
        '''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scaling_mode(self) -> typing.Optional[builtins.str]:
        '''The `scaling mode <https://cloud.google.com/run/docs/reference/rest/v2/projects.locations.services#scalingmode>`_ for the service. Possible values: ["AUTOMATIC", "MANUAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling_mode CloudRunV2Service#scaling_mode}
        '''
        result = self._values.get("scaling_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd5742acda2fd46c8fc7abd8ef6f04bc84b248ab63e36bf62564de55b61dfce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetManualInstanceCount")
    def reset_manual_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @jsii.member(jsii_name="resetScalingMode")
    def reset_scaling_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingMode", []))

    @builtins.property
    @jsii.member(jsii_name="manualInstanceCountInput")
    def manual_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "manualInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingModeInput")
    def scaling_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="manualInstanceCount")
    def manual_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "manualInstanceCount"))

    @manual_instance_count.setter
    def manual_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b575cd72d760ba807e4c37ec1ec8f75b2379315e530a1c6eebfe4988fcfb442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0401e737630b7274e2515e5f016f425b8811847727b603a4580ab8ed07bf682b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingMode")
    def scaling_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingMode"))

    @scaling_mode.setter
    def scaling_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8811b18a4d992037688b2b4d997450835ee52f9ff488c6de7acca28db0278ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceScaling]:
        return typing.cast(typing.Optional[CloudRunV2ServiceScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunV2ServiceScaling]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1174cfa446945167b17f9fb31568c5a7d1d69dde13bf57329142f4491449fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "containers": "containers",
        "encryption_key": "encryptionKey",
        "execution_environment": "executionEnvironment",
        "gpu_zonal_redundancy_disabled": "gpuZonalRedundancyDisabled",
        "labels": "labels",
        "max_instance_request_concurrency": "maxInstanceRequestConcurrency",
        "node_selector": "nodeSelector",
        "revision": "revision",
        "scaling": "scaling",
        "service_account": "serviceAccount",
        "session_affinity": "sessionAffinity",
        "timeout": "timeout",
        "volumes": "volumes",
        "vpc_access": "vpcAccess",
    },
)
class CloudRunV2ServiceTemplate:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        execution_environment: typing.Optional[builtins.str] = None,
        gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
        node_selector: typing.Optional[typing.Union["CloudRunV2ServiceTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        revision: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["CloudRunV2ServiceTemplateScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudRunV2ServiceTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 RevisionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#annotations CloudRunV2Service#annotations}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#containers CloudRunV2Service#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#encryption_key CloudRunV2Service#encryption_key}
        :param execution_environment: The sandbox environment to host this Revision. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#execution_environment CloudRunV2Service#execution_environment}
        :param gpu_zonal_redundancy_disabled: True if GPU zonal redundancy is disabled on this revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#gpu_zonal_redundancy_disabled CloudRunV2Service#gpu_zonal_redundancy_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 RevisionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#labels CloudRunV2Service#labels}
        :param max_instance_request_concurrency: Sets the maximum number of requests that each serving instance can receive. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#max_instance_request_concurrency CloudRunV2Service#max_instance_request_concurrency}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#node_selector CloudRunV2Service#node_selector}
        :param revision: The unique name for the revision. If this field is omitted, it will be automatically generated based on the Service name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#revision CloudRunV2Service#revision}
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling CloudRunV2Service#scaling}
        :param service_account: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service_account CloudRunV2Service#service_account}
        :param session_affinity: Enables session affinity. For more information, go to https://cloud.google.com/run/docs/configuring/session-affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#session_affinity CloudRunV2Service#session_affinity}
        :param timeout: Max allowed time for an instance to respond to a request. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout CloudRunV2Service#timeout}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#volumes CloudRunV2Service#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#vpc_access CloudRunV2Service#vpc_access}
        '''
        if isinstance(node_selector, dict):
            node_selector = CloudRunV2ServiceTemplateNodeSelector(**node_selector)
        if isinstance(scaling, dict):
            scaling = CloudRunV2ServiceTemplateScaling(**scaling)
        if isinstance(vpc_access, dict):
            vpc_access = CloudRunV2ServiceTemplateVpcAccess(**vpc_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d3bfca5e54a4d398ff775e01c980d9bced7479c7d0e1f004555612bf3fed1c)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument execution_environment", value=execution_environment, expected_type=type_hints["execution_environment"])
            check_type(argname="argument gpu_zonal_redundancy_disabled", value=gpu_zonal_redundancy_disabled, expected_type=type_hints["gpu_zonal_redundancy_disabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_instance_request_concurrency", value=max_instance_request_concurrency, expected_type=type_hints["max_instance_request_concurrency"])
            check_type(argname="argument node_selector", value=node_selector, expected_type=type_hints["node_selector"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument vpc_access", value=vpc_access, expected_type=type_hints["vpc_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if containers is not None:
            self._values["containers"] = containers
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if execution_environment is not None:
            self._values["execution_environment"] = execution_environment
        if gpu_zonal_redundancy_disabled is not None:
            self._values["gpu_zonal_redundancy_disabled"] = gpu_zonal_redundancy_disabled
        if labels is not None:
            self._values["labels"] = labels
        if max_instance_request_concurrency is not None:
            self._values["max_instance_request_concurrency"] = max_instance_request_concurrency
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if revision is not None:
            self._values["revision"] = revision
        if scaling is not None:
            self._values["scaling"] = scaling
        if service_account is not None:
            self._values["service_account"] = service_account
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if timeout is not None:
            self._values["timeout"] = timeout
        if volumes is not None:
            self._values["volumes"] = volumes
        if vpc_access is not None:
            self._values["vpc_access"] = vpc_access

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that may be set by external tools to store and arbitrary metadata.

        They are not queryable and should be preserved when modifying objects.

        Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system annotations in v1 now have a corresponding field in v2 RevisionTemplate.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#annotations CloudRunV2Service#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def containers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#containers CloudRunV2Service#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainers"]]], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''A reference to a customer managed encryption key (CMEK) to use to encrypt this container image.

        For more information, go to https://cloud.google.com/run/docs/securing/using-cmek

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#encryption_key CloudRunV2Service#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_environment(self) -> typing.Optional[builtins.str]:
        '''The sandbox environment to host this Revision. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#execution_environment CloudRunV2Service#execution_environment}
        '''
        result = self._values.get("execution_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_zonal_redundancy_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if GPU zonal redundancy is disabled on this revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#gpu_zonal_redundancy_disabled CloudRunV2Service#gpu_zonal_redundancy_disabled}
        '''
        result = self._values.get("gpu_zonal_redundancy_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc.
        For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 RevisionTemplate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#labels CloudRunV2Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_instance_request_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Sets the maximum number of requests that each serving instance can receive.

        If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#max_instance_request_concurrency CloudRunV2Service#max_instance_request_concurrency}
        '''
        result = self._values.get("max_instance_request_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_selector(self) -> typing.Optional["CloudRunV2ServiceTemplateNodeSelector"]:
        '''node_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#node_selector CloudRunV2Service#node_selector}
        '''
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateNodeSelector"], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''The unique name for the revision.

        If this field is omitted, it will be automatically generated based on the Service name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#revision CloudRunV2Service#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling(self) -> typing.Optional["CloudRunV2ServiceTemplateScaling"]:
        '''scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#scaling CloudRunV2Service#scaling}
        '''
        result = self._values.get("scaling")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateScaling"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Email address of the IAM service account associated with the revision of the service.

        The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service_account CloudRunV2Service#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables session affinity. For more information, go to https://cloud.google.com/run/docs/configuring/session-affinity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#session_affinity CloudRunV2Service#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Max allowed time for an instance to respond to a request.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout CloudRunV2Service#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#volumes CloudRunV2Service#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVolumes"]]], result)

    @builtins.property
    def vpc_access(self) -> typing.Optional["CloudRunV2ServiceTemplateVpcAccess"]:
        '''vpc_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#vpc_access CloudRunV2Service#vpc_access}
        '''
        result = self._values.get("vpc_access")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVpcAccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainers",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "base_image_uri": "baseImageUri",
        "command": "command",
        "depends_on": "dependsOn",
        "env": "env",
        "liveness_probe": "livenessProbe",
        "name": "name",
        "ports": "ports",
        "resources": "resources",
        "startup_probe": "startupProbe",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class CloudRunV2ServiceTemplateContainers:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        base_image_uri: typing.Optional[builtins.str] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateContainersEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        liveness_probe: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersLivenessProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersPorts", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersResources", typing.Dict[builtins.str, typing.Any]]] = None,
        startup_probe: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: URL of the Container image in Google Container Registry or Google Artifact Registry. More info: https://kubernetes.io/docs/concepts/containers/images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#image CloudRunV2Service#image}
        :param args: Arguments to the entrypoint. The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#args CloudRunV2Service#args}
        :param base_image_uri: Base image for this container. If set, it indicates that the service is enrolled into automatic base image update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#base_image_uri CloudRunV2Service#base_image_uri}
        :param command: Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#command CloudRunV2Service#command}
        :param depends_on: Containers which should be started before this container. If specified the container will wait to start until all containers with the listed names are healthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#depends_on CloudRunV2Service#depends_on}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#env CloudRunV2Service#env}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#liveness_probe CloudRunV2Service#liveness_probe}
        :param name: Name of the container specified as a DNS_LABEL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#ports CloudRunV2Service#ports}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#resources CloudRunV2Service#resources}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#startup_probe CloudRunV2Service#startup_probe}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#volume_mounts CloudRunV2Service#volume_mounts}
        :param working_dir: Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#working_dir CloudRunV2Service#working_dir}
        '''
        if isinstance(liveness_probe, dict):
            liveness_probe = CloudRunV2ServiceTemplateContainersLivenessProbe(**liveness_probe)
        if isinstance(ports, dict):
            ports = CloudRunV2ServiceTemplateContainersPorts(**ports)
        if isinstance(resources, dict):
            resources = CloudRunV2ServiceTemplateContainersResources(**resources)
        if isinstance(startup_probe, dict):
            startup_probe = CloudRunV2ServiceTemplateContainersStartupProbe(**startup_probe)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86329e372ec653fd4dbecd19295fcd59fb3469401986cc665947a12287e3d34c)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument base_image_uri", value=base_image_uri, expected_type=type_hints["base_image_uri"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument liveness_probe", value=liveness_probe, expected_type=type_hints["liveness_probe"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument startup_probe", value=startup_probe, expected_type=type_hints["startup_probe"])
            check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
            check_type(argname="argument working_dir", value=working_dir, expected_type=type_hints["working_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if args is not None:
            self._values["args"] = args
        if base_image_uri is not None:
            self._values["base_image_uri"] = base_image_uri
        if command is not None:
            self._values["command"] = command
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if env is not None:
            self._values["env"] = env
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if name is not None:
            self._values["name"] = name
        if ports is not None:
            self._values["ports"] = ports
        if resources is not None:
            self._values["resources"] = resources
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def image(self) -> builtins.str:
        '''URL of the Container image in Google Container Registry or Google Artifact Registry. More info: https://kubernetes.io/docs/concepts/containers/images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#image CloudRunV2Service#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the entrypoint.

        The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#args CloudRunV2Service#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def base_image_uri(self) -> typing.Optional[builtins.str]:
        '''Base image for this container. If set, it indicates that the service is enrolled into automatic base image update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#base_image_uri CloudRunV2Service#base_image_uri}
        '''
        result = self._values.get("base_image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Entrypoint array.

        Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#command CloudRunV2Service#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Containers which should be started before this container.

        If specified the container will wait to start until all containers with the listed names are healthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#depends_on CloudRunV2Service#depends_on}
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#env CloudRunV2Service#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersEnv"]]], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbe"]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#liveness_probe CloudRunV2Service#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbe"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the container specified as a DNS_LABEL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(self) -> typing.Optional["CloudRunV2ServiceTemplateContainersPorts"]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#ports CloudRunV2Service#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersPorts"], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#resources CloudRunV2Service#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersResources"], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbe"]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#startup_probe CloudRunV2Service#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbe"], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#volume_mounts CloudRunV2Service#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersVolumeMounts"]]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Container's working directory.

        If not specified, the container runtime's default will be used, which might be configured in the container image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#working_dir CloudRunV2Service#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersBuildInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2ServiceTemplateContainersBuildInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersBuildInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersBuildInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersBuildInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e987b8443520d78f214d89d22153a16202862297a0dd3ad3dec2ff1f8ee01942)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateContainersBuildInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24fc45fa5526e97a3d1e65ed05282e74390b428dc008c9e99430e3a7de142b27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateContainersBuildInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96687a146237c0828d5d7c7c12b86d573f827f7133b9dc7ff6b668a5941b863)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79327edcb318d46f7f33ec19cc9e69f650c386a41a77dd479e52a60ccdca4cc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ffe278e87e01c6b8752cd8f9d1ab1eb868b3bbb64549281a1d9900bdda49266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersBuildInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersBuildInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6afeaa7f50238235ba56d47af09e9f302f7e826e5802ce50c53276ae53fa4d56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="functionTarget")
    def function_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionTarget"))

    @builtins.property
    @jsii.member(jsii_name="sourceLocation")
    def source_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceLocation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersBuildInfo]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersBuildInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersBuildInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8247a7903111c1847148e2c74ab73b1c8615d7f921a47f793c5c733859356e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_source": "valueSource"},
)
class CloudRunV2ServiceTemplateContainersEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
        value_source: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersEnvValueSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a C_IDENTIFIER, and may not exceed 32768 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        :param value: Literal value of the environment variable. Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value CloudRunV2Service#value}
        :param value_source: value_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value_source CloudRunV2Service#value_source}
        '''
        if isinstance(value_source, dict):
            value_source = CloudRunV2ServiceTemplateContainersEnvValueSource(**value_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffcb3dd8d3e3abb15f91d9bd100bf1586561281aecf86a24472f10f87befab38)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument value_source", value=value_source, expected_type=type_hints["value_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value
        if value_source is not None:
            self._values["value_source"] = value_source

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the environment variable. Must be a C_IDENTIFIER, and may not exceed 32768 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Literal value of the environment variable.

        Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value CloudRunV2Service#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_source(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSource"]:
        '''value_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value_source CloudRunV2Service#value_source}
        '''
        result = self._values.get("value_source")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd16a4c06d3f1713dbb452774367a57addbdc8d91e6d793f1ac9d261dcb594d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateContainersEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f09f645eaa708490788d7e70648806dd23222978e0ebb0dae32444b2a6529e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateContainersEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a462e097ac3df2ad09425fc79157264034c1f31d50dbbfd2c057873b28d7556)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8778ceeaff98c08dd4dbcd5ddf3cf8302475ccbe86e362dbb215cd5df841215f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12b1a69187e3506f84279c3ea8f25810fb43ef0f63a300ede713db12e90909d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e86ff8627d05f2da0d4344f23f0a42c401b2566c0cc7ef702684d715b4aa6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e923eea11fb11cf64f3c795d1c449e5eaa57ec9cb1802e939ce2792ebd42d9c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueSource")
    def put_value_source(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret_key_ref CloudRunV2Service#secret_key_ref}
        '''
        value = CloudRunV2ServiceTemplateContainersEnvValueSource(
            secret_key_ref=secret_key_ref
        )

        return typing.cast(None, jsii.invoke(self, "putValueSource", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValueSource")
    def reset_value_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueSource", []))

    @builtins.property
    @jsii.member(jsii_name="valueSource")
    def value_source(
        self,
    ) -> "CloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference", jsii.get(self, "valueSource"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="valueSourceInput")
    def value_source_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSource"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSource"], jsii.get(self, "valueSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4a2c5a3e9cb04877002136d98867a4a0fcdb52e9cfa28d61cdbb198b201562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe47175d6d6c47416df98a5daa04fc224787a9dff8d344e507b8314df64655b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe56c873c84cec931a1179f226dd17ad2dfbab1f30930f8eef7825ba454288e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersEnvValueSource",
    jsii_struct_bases=[],
    name_mapping={"secret_key_ref": "secretKeyRef"},
)
class CloudRunV2ServiceTemplateContainersEnvValueSource:
    def __init__(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret_key_ref CloudRunV2Service#secret_key_ref}
        '''
        if isinstance(secret_key_ref, dict):
            secret_key_ref = CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef(**secret_key_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfee9b8c4add18efebba832664f9b448af80c724b4f05f057b8f65a1179d01f)
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_key_ref is not None:
            self._values["secret_key_ref"] = secret_key_ref

    @builtins.property
    def secret_key_ref(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"]:
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret_key_ref CloudRunV2Service#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersEnvValueSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eae2d66fa9e69f53fcb54a159608bf9a966668577358182e268e8e0fd9d24357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretKeyRef")
    def put_secret_key_ref(
        self,
        *,
        secret: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#version CloudRunV2Service#version}
        '''
        value = CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef(
            secret=secret, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretKeyRef", [value]))

    @jsii.member(jsii_name="resetSecretKeyRef")
    def reset_secret_key_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKeyRef", []))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRef")
    def secret_key_ref(
        self,
    ) -> "CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSource]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153e41156d83cadfa414b4567c5cb0bc8a94877627861d881dabcf007caea063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "version": "version"},
)
class CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef:
    def __init__(
        self,
        *,
        secret: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#version CloudRunV2Service#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d635373b9140e0dfd31a4e7f3a7b80c11182c2f8308cfcb2c10b84cc990931f6)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def secret(self) -> builtins.str:
        '''The name of the secret in Cloud Secret Manager.

        Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#version CloudRunV2Service#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1c70a0c572dd75e750d6db2279edb636662a78ce06d127b4d028f535ddd13b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e2beee642ad85b50933ebb057a0e1a53c7dabbadc8b7206707e634c663c34d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5968add9ee1baa40915be34c24bf45481f71cb66508e38951cc11f9e521f85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c36ce0b21d76181c96d6894bb328b12f1b0ff7ddb77cfdf64f359fcb471bc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1189a1c7d59bb30a3bed145c98e910a41b6014113a86307eeb78124c57c904c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21795d6278af2e47bb893d9016d873226a993250d82cd5ed3cde216b2eb96c46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143f2b81f929a8e219c06f8570bd794d0b86ff98d0e5bf5477c70f85a9092e91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b83f53819fe49601ce199a18afbd106ed9a18341032e5aa7df62b4837527c704)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fc13b7cc3f684f0a4e233c818e8e72dcfc0b083f5489c305ea853503faf5146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d685c248fe4da1abb9e6a1439041442724194417a41039494d342d322e2389b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbe",
    jsii_struct_bases=[],
    name_mapping={
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "tcp_socket": "tcpSocket",
        "timeout_seconds": "timeoutSeconds",
    },
)
class CloudRunV2ServiceTemplateContainersLivenessProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersLivenessProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#failure_threshold CloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#grpc CloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_get CloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#initial_delay_seconds CloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#period_seconds CloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tcp_socket CloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout_seconds CloudRunV2Service#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = CloudRunV2ServiceTemplateContainersLivenessProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52275fafcd3e7caf04971686c6905b28f5ed6b94eb125b4c3b92548a627216d)
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument tcp_socket", value=tcp_socket, expected_type=type_hints["tcp_socket"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if tcp_socket is not None:
            self._values["tcp_socket"] = tcp_socket
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Minimum consecutive failures for the probe to be considered failed after having succeeded.

        Defaults to 3. Minimum value is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#failure_threshold CloudRunV2Service#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#grpc CloudRunV2Service#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_get CloudRunV2Service#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#initial_delay_seconds CloudRunV2Service#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#period_seconds CloudRunV2Service#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tcp_socket CloudRunV2Service#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout_seconds CloudRunV2Service#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class CloudRunV2ServiceTemplateContainersLivenessProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service CloudRunV2Service#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c9e7a7f06cffdd5d46ab0da907df48ac8da868109891497dcad83befdf4166)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service CloudRunV2Service#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersLivenessProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__687e10d1a428b4a29d3ac604c229ccc3725b2e5e7626ca21067c9084408f2fed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068d7c0bfc6af11d2f7511c1946ccd64c25447703461237af9da79e4c3f35b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb1321c7b28ab7272a3f50ee0969286b7c9c9d5c5c40f4d377e8f2dd09c5b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fda1dfdaf8634723a48b902c4fdc2bafc512b2b6906f8dd488822b96ff479d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_headers CloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a41601b4ce807560c09857847be36887e4351504a0ffead63acc54e831d57c6)
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_headers CloudRunV2Service#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. Defaults to '/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value CloudRunV2Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c64d7551982d384af893a6dd5b9a1917dd28917b65b3b0dbfde3753bedfb2c0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The header field name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value CloudRunV2Service#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__458df13be69532b2a778dca0cbf13fe4e26765bacf1341ac02a9a1adbe379832)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9428300b40634e8a2146521ab3ebf1682a9cd9b84878d346bab3c64d20fe80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950a6e490203f8aa931666a652e9081b8e0f3b01aa80602c5200423d024faa20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c68a6da08fe2d10fa2fd2f7cc4a98fcb73f4fb62790823fdb9eeeb94e01cc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14a2f0ff679b7f5905468b0b170e372d339e76040ceb08a83efe3c4ad530f99e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf138b91906352d98fcb887aff6222ccd29d367f61ba1bb641f0224d065d912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c192e599dc8036cf03aea3768198b1d5914d80aabb7762cc83a111bc1cf2083d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b34c90d685ff838b09de91b27ff7135e63e8aa1d6b38743db662ec15c6c0fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b21f353364275bf49da1b6bd00a601bb4d2ab8d7037c4e19185f5f28c2e546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0253524c4807719afa70fbdc1cb0a0cdbaa02ddcc7ac8a54c176aa15280edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42655f0df5f328c995ee5ffdba55af8681e32996e20dcae768c668dbbc04272d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460da7085bf42824c45af26e124b91eab92f326e23c982b051c9e3f7bcaf4228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList:
        return typing.cast(CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef55fb24ca5590fcb5cb122cc15373ba955573252da58b92f9a6f3b1de639e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d7199056c234b78183e7edaa26b812a498e3d7a6d28a2e7a463bdbe860936f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beea5a8b9e375aa215f3a776f24d820bface90610a532f181e6ba8213e1ffca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9930ae9371c403b2b8ffba4cacdd50143efd1e5d86547b2b958b63b4498f520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service CloudRunV2Service#service}
        '''
        value = CloudRunV2ServiceTemplateContainersLivenessProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_headers CloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        value = CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(self, *, port: jsii.Number) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the exposed port of the container, which is the value of container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        value = CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket(port=port)

        return typing.cast(None, jsii.invoke(self, "putTcpSocket", [value]))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetTcpSocket")
    def reset_tcp_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpSocket", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> CloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocketInput")
    def tcp_socket_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702ab29382c0470c6588c60456cadbbd36a4ab3969ebf801b57ac48e9ff00ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e95ae97e94b30666475ae4790a6a29e2dea16b0f36f54e17f6c82019c1f9260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac28a481005e129553521ff682043ce2ab8468b44c72f28422fd31b3d23408a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38aa3073d036fbcfaccf2dcba7a662365afc89e507d98a3280792fc3032fffce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbe]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec53bc311869dbb6bc76b176cd1feee77a57bfeda99f6800ea773fb285251965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket:
    def __init__(self, *, port: jsii.Number) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the exposed port of the container, which is the value of container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50268e56be1e9096a04e10de375aaae39dd5489e659ae97a8ea916709ae9b4df)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Port number to access on the container.

        Must be in the range 1 to 65535.
        If not specified, defaults to the exposed port of the container, which
        is the value of container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08ce602198b5691dc08bcc3d616b6156e0c7b13dfd640e2861b53ad727099e21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b4bcef94a2e3f694a8831d71e0c590057dcdd14d02b2eb05a07b155977003e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b92fc43daa7df77c3a7620c1a37d452477db2739aed953d2176bbe003e1060f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81bc1af1490110259961e18236df3e92a26a37ca6fd3389b793eebe01476d195)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61b51bdfaece5a30695c6cb667c13a54a5aabdd47653861e2bdfe0c56d8cf7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putLivenessProbe")
    def put_liveness_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#failure_threshold CloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#grpc CloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_get CloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#initial_delay_seconds CloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#period_seconds CloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tcp_socket CloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout_seconds CloudRunV2Service#timeout_seconds}
        '''
        value = CloudRunV2ServiceTemplateContainersLivenessProbe(
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putLivenessProbe", [value]))

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        *,
        container_port: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_port: Port number the container listens on. This must be a valid TCP port number, 0 < containerPort < 65536. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#container_port CloudRunV2Service#container_port}
        :param name: If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        value = CloudRunV2ServiceTemplateContainersPorts(
            container_port=container_port, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        cpu_idle: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        startup_cpu_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cpu_idle: Determines whether CPU is only allocated during requests. True by default if the parent 'resources' field is not set. However, if 'resources' is set, this field must be explicitly set to true to preserve the default behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#cpu_idle CloudRunV2Service#cpu_idle}
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#limits CloudRunV2Service#limits}
        :param startup_cpu_boost: Determines whether CPU should be boosted on startup of a new container instance above the requested CPU threshold, this can help reduce cold-start latency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#startup_cpu_boost CloudRunV2Service#startup_cpu_boost}
        '''
        value = CloudRunV2ServiceTemplateContainersResources(
            cpu_idle=cpu_idle, limits=limits, startup_cpu_boost=startup_cpu_boost
        )

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#failure_threshold CloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#grpc CloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_get CloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#initial_delay_seconds CloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#period_seconds CloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tcp_socket CloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout_seconds CloudRunV2Service#timeout_seconds}
        '''
        value = CloudRunV2ServiceTemplateContainersStartupProbe(
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putStartupProbe", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e78cb6f27530c26e24715b25484a9a03b9bfa56529ed66eadfe36409dab284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetBaseImageUri")
    def reset_base_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseImageUri", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetDependsOn")
    def reset_depends_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependsOn", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetLivenessProbe")
    def reset_liveness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivenessProbe", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetStartupProbe")
    def reset_startup_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupProbe", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

    @builtins.property
    @jsii.member(jsii_name="buildInfo")
    def build_info(self) -> CloudRunV2ServiceTemplateContainersBuildInfoList:
        return typing.cast(CloudRunV2ServiceTemplateContainersBuildInfoList, jsii.get(self, "buildInfo"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> CloudRunV2ServiceTemplateContainersEnvList:
        return typing.cast(CloudRunV2ServiceTemplateContainersEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(
        self,
    ) -> CloudRunV2ServiceTemplateContainersLivenessProbeOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateContainersLivenessProbeOutputReference, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "CloudRunV2ServiceTemplateContainersPortsOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateContainersPortsOutputReference", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "CloudRunV2ServiceTemplateContainersResourcesOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateContainersResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(
        self,
    ) -> "CloudRunV2ServiceTemplateContainersStartupProbeOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateContainersStartupProbeOutputReference", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(self) -> "CloudRunV2ServiceTemplateContainersVolumeMountsList":
        return typing.cast("CloudRunV2ServiceTemplateContainersVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="baseImageUriInput")
    def base_image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseImageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="dependsOnInput")
    def depends_on_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependsOnInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbeInput")
    def liveness_probe_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbe]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbe], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersPorts"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersPorts"], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersResources"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbe"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbe"], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirInput")
    def working_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80eeced003b878b2746b8f290baded961bf47ac5d1ef6ec758c29d4079e8e23f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseImageUri")
    def base_image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseImageUri"))

    @base_image_uri.setter
    def base_image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71632689be500bd2bdbe5d53569065a4025110dc0d1eb6c5c57c6401a23791f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseImageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9ff1924dde182574f947d258e0db6b4f4737e889307ef430be180d8c4dc273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffcf159f9e2908c8115bbb65a2d9e78b5b62cd28e2f2032f41db9b84de3e4644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0deb5d61f4a6234a6cc3d78ec7c4356afbff25ad699dbb30873484a6ad8634ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0307679ae2963708f7e3047ded1d33538dca4475693c2f27689bf63efbba1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c631de891cc696b6612ec7bbbab22f293c79d7dcc5799819890df763a800dcb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121df78a03ec00928c88ef68b7e63bbacba280975faad1581cb414bde5cf3fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersPorts",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort", "name": "name"},
)
class CloudRunV2ServiceTemplateContainersPorts:
    def __init__(
        self,
        *,
        container_port: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_port: Port number the container listens on. This must be a valid TCP port number, 0 < containerPort < 65536. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#container_port CloudRunV2Service#container_port}
        :param name: If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23de5fbdb1a131c1121443263fcd0f538e3a80d6b1f01e57c0d55dcf8136376d)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_port is not None:
            self._values["container_port"] = container_port
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''Port number the container listens on. This must be a valid TCP port number, 0 < containerPort < 65536.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#container_port CloudRunV2Service#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15980028acf2fe3f6f90a259cd5104622094e29d2342e1ee2f7ad7ce7e334426)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerPort")
    def reset_container_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerPort", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="containerPortInput")
    def container_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerPort"))

    @container_port.setter
    def container_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76559724f4fb7bd5dc88000c653f71f5c2264d7272b64c2d389500fde510373c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dba8a96945ab8684bfd2410baa8627a8685182bd529ed46d886cc851578951b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersPorts]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersPorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersPorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f99dc3baf3730e7f87a0ee43f55c5c924d9a25d82ddfbb9e8be24fd51843e34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersResources",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_idle": "cpuIdle",
        "limits": "limits",
        "startup_cpu_boost": "startupCpuBoost",
    },
)
class CloudRunV2ServiceTemplateContainersResources:
    def __init__(
        self,
        *,
        cpu_idle: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        startup_cpu_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cpu_idle: Determines whether CPU is only allocated during requests. True by default if the parent 'resources' field is not set. However, if 'resources' is set, this field must be explicitly set to true to preserve the default behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#cpu_idle CloudRunV2Service#cpu_idle}
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#limits CloudRunV2Service#limits}
        :param startup_cpu_boost: Determines whether CPU should be boosted on startup of a new container instance above the requested CPU threshold, this can help reduce cold-start latency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#startup_cpu_boost CloudRunV2Service#startup_cpu_boost}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170b8a4fb2157a238737d366cd7c416ba8eb444e4daed3859935310674a49f61)
            check_type(argname="argument cpu_idle", value=cpu_idle, expected_type=type_hints["cpu_idle"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument startup_cpu_boost", value=startup_cpu_boost, expected_type=type_hints["startup_cpu_boost"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_idle is not None:
            self._values["cpu_idle"] = cpu_idle
        if limits is not None:
            self._values["limits"] = limits
        if startup_cpu_boost is not None:
            self._values["startup_cpu_boost"] = startup_cpu_boost

    @builtins.property
    def cpu_idle(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether CPU is only allocated during requests.

        True by default if the parent 'resources' field is not set. However, if
        'resources' is set, this field must be explicitly set to true to preserve the default behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#cpu_idle CloudRunV2Service#cpu_idle}
        '''
        result = self._values.get("cpu_idle")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def limits(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#limits CloudRunV2Service#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def startup_cpu_boost(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether CPU should be boosted on startup of a new container instance above the requested CPU threshold, this can help reduce cold-start latency.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#startup_cpu_boost CloudRunV2Service#startup_cpu_boost}
        '''
        result = self._values.get("startup_cpu_boost")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fef5cd008c0b5cf424e4df15dab4422290fdbd09395902e8910415d4587494d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuIdle")
    def reset_cpu_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuIdle", []))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetStartupCpuBoost")
    def reset_startup_cpu_boost(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupCpuBoost", []))

    @builtins.property
    @jsii.member(jsii_name="cpuIdleInput")
    def cpu_idle_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuIdleInput"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="startupCpuBoostInput")
    def startup_cpu_boost_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startupCpuBoostInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuIdle")
    def cpu_idle(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cpuIdle"))

    @cpu_idle.setter
    def cpu_idle(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb0ce3d4493ab3867c7982292fb1319d6b645c4821d789f2832b197104b9052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuIdle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "limits"))

    @limits.setter
    def limits(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85888149006d451fc648cb3834510c09ea1a084ab80c58735c13c2f692b737e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startupCpuBoost")
    def startup_cpu_boost(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startupCpuBoost"))

    @startup_cpu_boost.setter
    def startup_cpu_boost(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b6a3741556cc5de2208e4a55fb96af3a94d2d5d683ccae93dce9adaffd94b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startupCpuBoost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersResources]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45dc67d8a24219b8e5953aee02e73595e1631d9cc84412451b2704a1a66a25ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbe",
    jsii_struct_bases=[],
    name_mapping={
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "tcp_socket": "tcpSocket",
        "timeout_seconds": "timeoutSeconds",
    },
)
class CloudRunV2ServiceTemplateContainersStartupProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#failure_threshold CloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#grpc CloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_get CloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#initial_delay_seconds CloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#period_seconds CloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tcp_socket CloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout_seconds CloudRunV2Service#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = CloudRunV2ServiceTemplateContainersStartupProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = CloudRunV2ServiceTemplateContainersStartupProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66729538d9e7414f7d58e4480760575ecf0a7787f3d6796ae46a770fdbeebbb)
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument tcp_socket", value=tcp_socket, expected_type=type_hints["tcp_socket"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if tcp_socket is not None:
            self._values["tcp_socket"] = tcp_socket
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Minimum consecutive failures for the probe to be considered failed after having succeeded.

        Defaults to 3. Minimum value is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#failure_threshold CloudRunV2Service#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#grpc CloudRunV2Service#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_get CloudRunV2Service#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#initial_delay_seconds CloudRunV2Service#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#period_seconds CloudRunV2Service#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tcp_socket CloudRunV2Service#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#timeout_seconds CloudRunV2Service#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class CloudRunV2ServiceTemplateContainersStartupProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service CloudRunV2Service#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8232faee8feeffdd572bc194c82ce02d9a8255068c7df085c5e41b9998405d23)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service CloudRunV2Service#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersStartupProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51168a0c7843bd214ceffa916c1296c790f0cbedca9f7c30344e312ea4c05a62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9f0616dab5f3afb74979f879a954506bdbfd939d3a1a6704e38f63801db664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d774dce998e527d95a770fa3fce2064287fb0c039e3d5eaa76583abc119855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ca85563d394a4c2c0bd43fa090b91da33883f8564bf5030418670bfee02452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class CloudRunV2ServiceTemplateContainersStartupProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_headers CloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319de96cd4fd21045e6bc211ee50fbe3a5afcdbce57ef133b7df59265866f0b1)
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_headers CloudRunV2Service#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. Defaults to '/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersStartupProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value CloudRunV2Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad8bb5565393dd68347af127fa0e591642ad5a10b9c8a41612ff8e4004a9c35)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The header field name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#value CloudRunV2Service#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba6593775bedd8328ec9d4f67793a9e033ca0fda163469e597c166777ea040eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c847a9ed5b99588d67f78d5fd4c9d4e244a02eee20b2db8ab96c83e3b9e6a415)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484e350d74384436a6da9e927ad72253da1e3240aa010f1cb5446bea138998d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f2852deca235aea8096ebb8caa5d44e8c4eae23248c85f43a24d07a071e25b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61fefea252665cc57cc23246d7512c149d6c2a84e8fec9a6dc0d9cbfca260562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9732be975b5f765c6a332c953d2393b21b597f39007ab036b9c16e0d10e78e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b256ad3b332fd9d345308427983f54bf2b051b0d1d16cb82b899a3997ee37e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc5bf6fae3108f32a303bd5ebb84f37079c4be2fa2994b66d9a3be3e4753dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5110e707c9e78ba18d6787e1e4d65f7b61e932b76cece0fc2bd3486c0b94378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c38db02b6e17b228591a854673af6fea2d3ff5d98f04e2365efb48d062cf743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edc89b55938de68bd1cb9300f0fcec2aadad1e0e169a564fdd6d6da96edb201f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b330b30f1317e706935704e2a2d2892ee862a210dff6ab27c331ab6ec4c1ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList:
        return typing.cast(CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2ff699f5fd8f7f99a94dab4495e2749cabf2af7253a5af33ba2de186606b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d80edb49872fe9995f42c285e47c673cd9d4bc87ae530fe5afe0a5846a46fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa344877b1b12dc753134195a46ea5a97b75aabc4b38500765055d07c86ec42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__877f260601b1d9059466ab5f367858051d7dadbeb0c3fa33d76c181180887a43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#service CloudRunV2Service#service}
        '''
        value = CloudRunV2ServiceTemplateContainersStartupProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#http_headers CloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        value = CloudRunV2ServiceTemplateContainersStartupProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        value = CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket(port=port)

        return typing.cast(None, jsii.invoke(self, "putTcpSocket", [value]))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetTcpSocket")
    def reset_tcp_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpSocket", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> CloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> CloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "CloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocketInput")
    def tcp_socket_input(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998218ef6f620b60c2621fff442d60e1218bc90264f4a03dc05572ced612b1f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d79f7604cd0888c358b03a86d45072f1896c2d2b7af86e57c7ca1a0f1e3ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd0cfd72a7c2d19dbe661b8142a34170faf879be41290986f6ea7bba0bb8b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48d4186d9a20c76d0a77b162c3b8bd0d75a645d3f944a8c7538fcdb98d9451c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbe]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af576ff187d081a09f409b86016a2f981cef538757290b2c21cf80af2befc54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket:
    def __init__(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8648255c5fbec5568045e56df2a3da21083077c017bee63937215b431c3f89)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#port CloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__226a907a4fe33b080ac2286ffb90d598953fe0ea4453f47a4d20cbdc5de68830)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c78859d5f0e2a9ee09fd32a613da4984798699aa0ed19a92e0b144523df3b51e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe64da29e82a74df5caa96c3e319efaa6369646bbe06b205ae28c87e9c8a2039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"mount_path": "mountPath", "name": "name"},
)
class CloudRunV2ServiceTemplateContainersVolumeMounts:
    def __init__(self, *, mount_path: builtins.str, name: builtins.str) -> None:
        '''
        :param mount_path: Path within the container at which the volume should be mounted. Must not contain ':'. For Cloud SQL volumes, it can be left empty, or must otherwise be /cloudsql. All instances defined in the Volume will be available as /cloudsql/[instance]. For more information on Cloud SQL volumes, visit https://cloud.google.com/sql/docs/mysql/connect-run Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#mount_path CloudRunV2Service#mount_path}
        :param name: This must match the Name of a Volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c249fc6e4b259c842313efa82e9077b9ce3fa6c4fffecc4e1b844e3d1b8cb04)
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mount_path": mount_path,
            "name": name,
        }

    @builtins.property
    def mount_path(self) -> builtins.str:
        '''Path within the container at which the volume should be mounted.

        Must not contain ':'. For Cloud SQL volumes, it can be left empty, or must otherwise be /cloudsql. All instances defined in the Volume will be available as /cloudsql/[instance]. For more information on Cloud SQL volumes, visit https://cloud.google.com/sql/docs/mysql/connect-run

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#mount_path CloudRunV2Service#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''This must match the Name of a Volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateContainersVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateContainersVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a592bee5333c30d746a255edcf9a8f3b8a65f79200c3537b0cea42dfadb0a92b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateContainersVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fe114314e439aadcd91f20850a082d9b7104988ab954376241715c64814545)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateContainersVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8383744a8a923d186866a862e3d2b6326e325641a8a3bb90f70993a817eac14e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dabea0345d75428fd9998d45ae46e960177513a1057e3383092c08d48865f58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65241fa473cc33154e1cb8dc9a81f3e9f3b6148ef16450947c4642230b536724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7b8d30a0a6b37f96cf2bf053edf4bac9cfc21eb6b64af98c39a136ce8fb427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateContainersVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateContainersVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f38794680763ca9839b37e85a7f47209b759c055589614dff66848637d0d7e9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b92de0b46994cb554e29fc1559fcc04c32c7d944492e7e1a4d82e985a914d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4467a78fcf2cce19b519774da0ff18ad850d7a8eebc9bbab75e2f4349e55c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0857e048981e774020c2d62f41788cea4e99046c172073a83e5695a30810faae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateNodeSelector",
    jsii_struct_bases=[],
    name_mapping={"accelerator": "accelerator"},
)
class CloudRunV2ServiceTemplateNodeSelector:
    def __init__(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#accelerator CloudRunV2Service#accelerator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bab498950cecffe0689454cf2eb496d7a9d81d88e9ad7cee5c80fb0c669f968)
            check_type(argname="argument accelerator", value=accelerator, expected_type=type_hints["accelerator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator": accelerator,
        }

    @builtins.property
    def accelerator(self) -> builtins.str:
        '''The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#accelerator CloudRunV2Service#accelerator}
        '''
        result = self._values.get("accelerator")
        assert result is not None, "Required property 'accelerator' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateNodeSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateNodeSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateNodeSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__806eee9761de2d6942e7b89739868e46e96f0a0713f02bba2833460e6a19839a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="acceleratorInput")
    def accelerator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorInput"))

    @builtins.property
    @jsii.member(jsii_name="accelerator")
    def accelerator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accelerator"))

    @accelerator.setter
    def accelerator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1158268841df715efb59508fb6d9cdbc6e17558efff9536a7b4f4f669bf23d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accelerator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTemplateNodeSelector]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateNodeSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateNodeSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d2427be2e2849c5010bb68a5e957c8166a618b448f7139e5edd1a25ed5c041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf22ecc7cc1aa02345c743ff8271f9e8831da5fdd4d42c04ce6107e3c9869f79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4beb3bc9b7baceba5b29f95f3428ae2ec1fc001f5729024ee131f647f45e63b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="putNodeSelector")
    def put_node_selector(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#accelerator CloudRunV2Service#accelerator}
        '''
        value = CloudRunV2ServiceTemplateNodeSelector(accelerator=accelerator)

        return typing.cast(None, jsii.invoke(self, "putNodeSelector", [value]))

    @jsii.member(jsii_name="putScaling")
    def put_scaling(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instance_count: Maximum number of serving instances that this resource should have. Must not be less than minimum instance count. If absent, Cloud Run will calculate a default value based on the project's available container instances quota in the region and specified instance size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#max_instance_count CloudRunV2Service#max_instance_count}
        :param min_instance_count: Minimum number of serving instances that this resource should have. Defaults to 0. Must not be greater than maximum instance count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#min_instance_count CloudRunV2Service#min_instance_count}
        '''
        value = CloudRunV2ServiceTemplateScaling(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
        )

        return typing.cast(None, jsii.invoke(self, "putScaling", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7606affc926265aab9be20aba8bc206f8a0951d0082c31ee15b6c60c0d9bb925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="putVpcAccess")
    def put_vpc_access(
        self,
        *,
        connector: typing.Optional[builtins.str] = None,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connector: VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#connector CloudRunV2Service#connector}
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#egress CloudRunV2Service#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#network_interfaces CloudRunV2Service#network_interfaces}
        '''
        value = CloudRunV2ServiceTemplateVpcAccess(
            connector=connector, egress=egress, network_interfaces=network_interfaces
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccess", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetContainers")
    def reset_containers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainers", []))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetExecutionEnvironment")
    def reset_execution_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionEnvironment", []))

    @jsii.member(jsii_name="resetGpuZonalRedundancyDisabled")
    def reset_gpu_zonal_redundancy_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuZonalRedundancyDisabled", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxInstanceRequestConcurrency")
    def reset_max_instance_request_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceRequestConcurrency", []))

    @jsii.member(jsii_name="resetNodeSelector")
    def reset_node_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeSelector", []))

    @jsii.member(jsii_name="resetRevision")
    def reset_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevision", []))

    @jsii.member(jsii_name="resetScaling")
    def reset_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaling", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetVpcAccess")
    def reset_vpc_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccess", []))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> CloudRunV2ServiceTemplateContainersList:
        return typing.cast(CloudRunV2ServiceTemplateContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelector")
    def node_selector(self) -> CloudRunV2ServiceTemplateNodeSelectorOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateNodeSelectorOutputReference, jsii.get(self, "nodeSelector"))

    @builtins.property
    @jsii.member(jsii_name="scaling")
    def scaling(self) -> "CloudRunV2ServiceTemplateScalingOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateScalingOutputReference", jsii.get(self, "scaling"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "CloudRunV2ServiceTemplateVolumesList":
        return typing.cast("CloudRunV2ServiceTemplateVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccess")
    def vpc_access(self) -> "CloudRunV2ServiceTemplateVpcAccessOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateVpcAccessOutputReference", jsii.get(self, "vpcAccess"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainers]]], jsii.get(self, "containersInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="executionEnvironmentInput")
    def execution_environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionEnvironmentInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuZonalRedundancyDisabledInput")
    def gpu_zonal_redundancy_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gpuZonalRedundancyDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceRequestConcurrencyInput")
    def max_instance_request_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceRequestConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelectorInput")
    def node_selector_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateNodeSelector]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateNodeSelector], jsii.get(self, "nodeSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingInput")
    def scaling_input(self) -> typing.Optional["CloudRunV2ServiceTemplateScaling"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateScaling"], jsii.get(self, "scalingInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessInput")
    def vpc_access_input(self) -> typing.Optional["CloudRunV2ServiceTemplateVpcAccess"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVpcAccess"], jsii.get(self, "vpcAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1f350ba78b4a40782dd1d8448b05b0580941364d87aafd8acc9e59f95f0901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982aba328432493ea863ce14a9921564f4cc27acb246b652680efc3e7561b809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionEnvironment")
    def execution_environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionEnvironment"))

    @execution_environment.setter
    def execution_environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d83e7563016dab0cbeda86ce07d5b0593f9b57c77bc17f1a568cb1b5fec2e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuZonalRedundancyDisabled")
    def gpu_zonal_redundancy_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "gpuZonalRedundancyDisabled"))

    @gpu_zonal_redundancy_disabled.setter
    def gpu_zonal_redundancy_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca762004d9a772119e5c4023d793d18b0709ff24a0fb6199bf2557f4b241d4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuZonalRedundancyDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5e55d2f0aab0d578ea6930247ce9d3e86e84249ce11bfa661f14badc785534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceRequestConcurrency")
    def max_instance_request_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceRequestConcurrency"))

    @max_instance_request_concurrency.setter
    def max_instance_request_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40c628bd08fadba4418d1860669d63fa89fbc7bba8b642fb43f70ab742d5c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceRequestConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7275914ef6e09e17400be2d0cfa0e4e4c1e6fd2bfd57819aaeecc723a8af24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc300c4e6da700f3583d6b01e4d6e2d64ca84e6ae834fa56f4e31687e3dfd367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9012ef50ee970d0c99678a61a11359884789457d1e35819f75267b7f77bd9356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba86a093e9e0754232a3d3a1b6fe2864332487f0ea86184802023d4bc5013a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTemplate]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunV2ServiceTemplate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa5a14d240c941f45735498dc28360bc111ed3af810cfb9637ec2c5c75578f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
    },
)
class CloudRunV2ServiceTemplateScaling:
    def __init__(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instance_count: Maximum number of serving instances that this resource should have. Must not be less than minimum instance count. If absent, Cloud Run will calculate a default value based on the project's available container instances quota in the region and specified instance size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#max_instance_count CloudRunV2Service#max_instance_count}
        :param min_instance_count: Minimum number of serving instances that this resource should have. Defaults to 0. Must not be greater than maximum instance count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#min_instance_count CloudRunV2Service#min_instance_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1e5d8beed9bf83e7dca58ad699539d772fcf63f761d44e78f8c7a124052cb73)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of serving instances that this resource should have.

        Must not be less than minimum instance count. If absent, Cloud Run will calculate
        a default value based on the project's available container instances quota in the region and specified instance size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#max_instance_count CloudRunV2Service#max_instance_count}
        '''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of serving instances that this resource should have.

        Defaults to 0. Must not be greater than maximum instance count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#min_instance_count CloudRunV2Service#min_instance_count}
        '''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05543d3b59b21b2b97794e248048f3333c1c1554ff2ba120ac8cb4ff768348fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b008e985a52d4f6e4f5133861a4768a7118bbc27409fff3c03337017de436482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c750587991b7a87f008fd76ae421b025f74b5cc05a90fb600c4d82b178d8f888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTemplateScaling]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb858aef68c03e8eeae0897378ec1b0685b036668c7284f1f3bcee6adafb169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "cloud_sql_instance": "cloudSqlInstance",
        "empty_dir": "emptyDir",
        "gcs": "gcs",
        "nfs": "nfs",
        "secret": "secret",
    },
)
class CloudRunV2ServiceTemplateVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        cloud_sql_instance: typing.Optional[typing.Union["CloudRunV2ServiceTemplateVolumesCloudSqlInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        empty_dir: typing.Optional[typing.Union["CloudRunV2ServiceTemplateVolumesEmptyDir", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs: typing.Optional[typing.Union["CloudRunV2ServiceTemplateVolumesGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["CloudRunV2ServiceTemplateVolumesNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["CloudRunV2ServiceTemplateVolumesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Volume's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        :param cloud_sql_instance: cloud_sql_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#cloud_sql_instance CloudRunV2Service#cloud_sql_instance}
        :param empty_dir: empty_dir block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#empty_dir CloudRunV2Service#empty_dir}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#gcs CloudRunV2Service#gcs}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#nfs CloudRunV2Service#nfs}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        '''
        if isinstance(cloud_sql_instance, dict):
            cloud_sql_instance = CloudRunV2ServiceTemplateVolumesCloudSqlInstance(**cloud_sql_instance)
        if isinstance(empty_dir, dict):
            empty_dir = CloudRunV2ServiceTemplateVolumesEmptyDir(**empty_dir)
        if isinstance(gcs, dict):
            gcs = CloudRunV2ServiceTemplateVolumesGcs(**gcs)
        if isinstance(nfs, dict):
            nfs = CloudRunV2ServiceTemplateVolumesNfs(**nfs)
        if isinstance(secret, dict):
            secret = CloudRunV2ServiceTemplateVolumesSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b4af8d0c08ce6753e1dc6bcb6197154395aadfb247e9cb51e2223af888e9b0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cloud_sql_instance", value=cloud_sql_instance, expected_type=type_hints["cloud_sql_instance"])
            check_type(argname="argument empty_dir", value=empty_dir, expected_type=type_hints["empty_dir"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if cloud_sql_instance is not None:
            self._values["cloud_sql_instance"] = cloud_sql_instance
        if empty_dir is not None:
            self._values["empty_dir"] = empty_dir
        if gcs is not None:
            self._values["gcs"] = gcs
        if nfs is not None:
            self._values["nfs"] = nfs
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def name(self) -> builtins.str:
        '''Volume's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#name CloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_sql_instance(
        self,
    ) -> typing.Optional["CloudRunV2ServiceTemplateVolumesCloudSqlInstance"]:
        '''cloud_sql_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#cloud_sql_instance CloudRunV2Service#cloud_sql_instance}
        '''
        result = self._values.get("cloud_sql_instance")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVolumesCloudSqlInstance"], result)

    @builtins.property
    def empty_dir(self) -> typing.Optional["CloudRunV2ServiceTemplateVolumesEmptyDir"]:
        '''empty_dir block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#empty_dir CloudRunV2Service#empty_dir}
        '''
        result = self._values.get("empty_dir")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVolumesEmptyDir"], result)

    @builtins.property
    def gcs(self) -> typing.Optional["CloudRunV2ServiceTemplateVolumesGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#gcs CloudRunV2Service#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVolumesGcs"], result)

    @builtins.property
    def nfs(self) -> typing.Optional["CloudRunV2ServiceTemplateVolumesNfs"]:
        '''nfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#nfs CloudRunV2Service#nfs}
        '''
        result = self._values.get("nfs")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVolumesNfs"], result)

    @builtins.property
    def secret(self) -> typing.Optional["CloudRunV2ServiceTemplateVolumesSecret"]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVolumesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesCloudSqlInstance",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class CloudRunV2ServiceTemplateVolumesCloudSqlInstance:
    def __init__(
        self,
        *,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#instances CloudRunV2Service#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c07b9c8d709404c3db5645e73c792798a2760baad4c3fa0b37a353a7fa8f5bf)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instances is not None:
            self._values["instances"] = instances

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#instances CloudRunV2Service#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVolumesCloudSqlInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ae9d638833ad2b42e1e9a6742e298d3c7d8f02828944ec96cf8dbf9d4a4905)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstances")
    def reset_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstances", []))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ed89f402bf6b5bb790e614f1533f66b4d93d68ecd45d9368336c26fec2d99c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesCloudSqlInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateVolumesCloudSqlInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3b9c079d5e6677db8daae57207aeef6c15d7f160790795337a78ef3e01c421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesEmptyDir",
    jsii_struct_bases=[],
    name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
)
class CloudRunV2ServiceTemplateVolumesEmptyDir:
    def __init__(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#medium CloudRunV2Service#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#size_limit CloudRunV2Service#size_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b81d6657e220a8d8e8ce383ce73c0621a9f096f85b296b6ca92c8a12abfd69a)
            check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
            check_type(argname="argument size_limit", value=size_limit, expected_type=type_hints["size_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if medium is not None:
            self._values["medium"] = medium
        if size_limit is not None:
            self._values["size_limit"] = size_limit

    @builtins.property
    def medium(self) -> typing.Optional[builtins.str]:
        '''The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#medium CloudRunV2Service#medium}
        '''
        result = self._values.get("medium")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_limit(self) -> typing.Optional[builtins.str]:
        '''Limit on the storage usable by this EmptyDir volume.

        The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#size_limit CloudRunV2Service#size_limit}
        '''
        result = self._values.get("size_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVolumesEmptyDir(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateVolumesEmptyDirOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesEmptyDirOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dbaea608ef3c7537405bf8f8408f38b53700e7a788156245976ea95845f5f95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMedium")
    def reset_medium(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMedium", []))

    @jsii.member(jsii_name="resetSizeLimit")
    def reset_size_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeLimit", []))

    @builtins.property
    @jsii.member(jsii_name="mediumInput")
    def medium_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediumInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeLimitInput")
    def size_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "medium"))

    @medium.setter
    def medium(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751fa55750d08d96ad318419cdd23f4ed6a13cc3ba8182f019fee595a0be849d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "medium", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeLimit")
    def size_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeLimit"))

    @size_limit.setter
    def size_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2005e4da648050e56ede564cf115c8e0f03288f67fd7df7e45ecc232056d572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesEmptyDir], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateVolumesEmptyDir],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a13ed13aa8a4783a09e8a4a2f27ede3092e4f25a6e9dc8890eab0f8148f478b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "read_only": "readOnly"},
)
class CloudRunV2ServiceTemplateVolumesGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket: GCS Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#bucket CloudRunV2Service#bucket}
        :param read_only: If true, mount the GCS bucket as read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#read_only CloudRunV2Service#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e166bf27d195036a7bf898c441a07060080a504448035ae1760f4c43e4808c)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def bucket(self) -> builtins.str:
        '''GCS Bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#bucket CloudRunV2Service#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the GCS bucket as read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#read_only CloudRunV2Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVolumesGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateVolumesGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f884e577e08a17317f72656f18e6b5e365f1a49aebe5a4dc1dc4a8d52de2c352)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d8b44f2975fdd418d6f5c1040d58b90c1ad9f68059e2e08f768d3747f7f3bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0502642fc858e4fc4d2413cb8a4e3f6f7960108cfa666872412f4a0e8ce075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTemplateVolumesGcs]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateVolumesGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0080bbdf97ae78824e4abce1d15c552007f33f02df6ab6d626b6e1a19917ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8fbb91aed0776da440aec0ad605656fd94c16a5ee098f5503f0418b7c1e345)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7b708321d2dd8fdea88b041712b08521b3ce6c2529c5481ce0a2cb7beba879)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bd71e82d6e567a8b68468b5983f8e46f341a145052aaf9b083d5e5ff9521b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__158be5e084baf58f6026678ee6fb1284e08de39fb095a288053b3ec94485b9c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06117ec160ff430de98cbec2d7d4ca30c56a515250a98318c0f74a64977034fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f472b40bc696a8958a213fe838ec2c648044af8f123d3e5951e80abb8db3e454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesNfs",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "server": "server", "read_only": "readOnly"},
)
class CloudRunV2ServiceTemplateVolumesNfs:
    def __init__(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#server CloudRunV2Service#server}
        :param read_only: If true, mount the NFS volume as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#read_only CloudRunV2Service#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab320416f93fd331f740dc41d0a9a8563956b2fefb7869904af50daed6b0f35)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "server": server,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def path(self) -> builtins.str:
        '''Path that is exported by the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Hostname or IP address of the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#server CloudRunV2Service#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the NFS volume as read only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#read_only CloudRunV2Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVolumesNfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateVolumesNfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesNfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bffcc86bb646401f3e282c6e8c28c0c7ae6d8b63bf774283b9340da4deeff455)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4996bb1ec3fefdec5bab92cb295839904132f00603cbf08a756d5bd969ab034d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e5702b505944bbb7af619c14bb7bd836b940386508ccf59402071e6117246b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96705a74eda23d219f3f9d25d4d59066482bdb619133cb743c7f43f246c3a8fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTemplateVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesNfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateVolumesNfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b35a5b0c9f8c720d29ffcb94025d35fd38500cfba1c8626a158916302b2967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bafc5d22b4c515d2fac5353e63d73fc1b1d34b98c521329deb02ea8f2b1f8bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCloudSqlInstance")
    def put_cloud_sql_instance(
        self,
        *,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#instances CloudRunV2Service#instances}
        '''
        value = CloudRunV2ServiceTemplateVolumesCloudSqlInstance(instances=instances)

        return typing.cast(None, jsii.invoke(self, "putCloudSqlInstance", [value]))

    @jsii.member(jsii_name="putEmptyDir")
    def put_empty_dir(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#medium CloudRunV2Service#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#size_limit CloudRunV2Service#size_limit}
        '''
        value = CloudRunV2ServiceTemplateVolumesEmptyDir(
            medium=medium, size_limit=size_limit
        )

        return typing.cast(None, jsii.invoke(self, "putEmptyDir", [value]))

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket: GCS Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#bucket CloudRunV2Service#bucket}
        :param read_only: If true, mount the GCS bucket as read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#read_only CloudRunV2Service#read_only}
        '''
        value = CloudRunV2ServiceTemplateVolumesGcs(bucket=bucket, read_only=read_only)

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putNfs")
    def put_nfs(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#server CloudRunV2Service#server}
        :param read_only: If true, mount the NFS volume as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#read_only CloudRunV2Service#read_only}
        '''
        value = CloudRunV2ServiceTemplateVolumesNfs(
            path=path, server=server, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putNfs", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#default_mode CloudRunV2Service#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#items CloudRunV2Service#items}
        '''
        value = CloudRunV2ServiceTemplateVolumesSecret(
            secret=secret, default_mode=default_mode, items=items
        )

        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="resetCloudSqlInstance")
    def reset_cloud_sql_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlInstance", []))

    @jsii.member(jsii_name="resetEmptyDir")
    def reset_empty_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyDir", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetNfs")
    def reset_nfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfs", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstance")
    def cloud_sql_instance(
        self,
    ) -> CloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference, jsii.get(self, "cloudSqlInstance"))

    @builtins.property
    @jsii.member(jsii_name="emptyDir")
    def empty_dir(self) -> CloudRunV2ServiceTemplateVolumesEmptyDirOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateVolumesEmptyDirOutputReference, jsii.get(self, "emptyDir"))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(self) -> CloudRunV2ServiceTemplateVolumesGcsOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateVolumesGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="nfs")
    def nfs(self) -> CloudRunV2ServiceTemplateVolumesNfsOutputReference:
        return typing.cast(CloudRunV2ServiceTemplateVolumesNfsOutputReference, jsii.get(self, "nfs"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "CloudRunV2ServiceTemplateVolumesSecretOutputReference":
        return typing.cast("CloudRunV2ServiceTemplateVolumesSecretOutputReference", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstanceInput")
    def cloud_sql_instance_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesCloudSqlInstance], jsii.get(self, "cloudSqlInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyDirInput")
    def empty_dir_input(
        self,
    ) -> typing.Optional[CloudRunV2ServiceTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesEmptyDir], jsii.get(self, "emptyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(self) -> typing.Optional[CloudRunV2ServiceTemplateVolumesGcs]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsInput")
    def nfs_input(self) -> typing.Optional[CloudRunV2ServiceTemplateVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesNfs], jsii.get(self, "nfsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional["CloudRunV2ServiceTemplateVolumesSecret"]:
        return typing.cast(typing.Optional["CloudRunV2ServiceTemplateVolumesSecret"], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43985a35a63a731a666534448183a622eb0f244dad1fcf0cc218b0ff5f0e6cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce5832ab4ebf33c32f85e20360bfe055a960a266a6937906955b8a3e89469b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesSecret",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "default_mode": "defaultMode", "items": "items"},
)
class CloudRunV2ServiceTemplateVolumesSecret:
    def __init__(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#default_mode CloudRunV2Service#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#items CloudRunV2Service#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c4a8a9700d249af53962509f2c043af9ce26819d5d499dbd94c08572587fc7)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument default_mode", value=default_mode, expected_type=type_hints["default_mode"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }
        if default_mode is not None:
            self._values["default_mode"] = default_mode
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def secret(self) -> builtins.str:
        '''The name of the secret in Cloud Secret Manager.

        Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#secret CloudRunV2Service#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_mode(self) -> typing.Optional[jsii.Number]:
        '''Integer representation of mode bits to use on created files by default.

        Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#default_mode CloudRunV2Service#default_mode}
        '''
        result = self._values.get("default_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVolumesSecretItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#items CloudRunV2Service#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVolumesSecretItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVolumesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesSecretItems",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "mode": "mode", "version": "version"},
)
class CloudRunV2ServiceTemplateVolumesSecretItems:
    def __init__(
        self,
        *,
        path: builtins.str,
        mode: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The relative path of the secret in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        :param mode: Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal). If 0 or not set, the Volume's default mode will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#mode CloudRunV2Service#mode}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#version CloudRunV2Service#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7287078e264ddaf9b2da735b8f3e9167f755933518d0168641f4b0f98f382e98)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if mode is not None:
            self._values["mode"] = mode
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def path(self) -> builtins.str:
        '''The relative path of the secret in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#path CloudRunV2Service#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        '''Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal).

        If 0 or not set, the Volume's default mode will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#mode CloudRunV2Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#version CloudRunV2Service#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVolumesSecretItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateVolumesSecretItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesSecretItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad674ab7150e54ae60def16177a399d098cb80f1370a31448a717bdd7b92d80f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateVolumesSecretItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b934e958cc729c248297f9ea8674849177bc70afe8bf365705c7b9d89251d31)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateVolumesSecretItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9cdc44c0e6a1949d42eae56b30bb466ab23d8f5e1b3cfb539ebeb570b5080f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5120128a0377888fa7c0b852ef0fa4c852aeb4a69eee8c83ef98ae36981d520b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1016326e9cc63a810d2e18f2825aa8cf154ba7c17c6d8b451e1bdfdccc5a9abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumesSecretItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumesSecretItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc0d7076ad3e88e36d0cb7d170b122a1ea3e58cb18cfa8ddd27e9935c8c73d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateVolumesSecretItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesSecretItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__653f5f7b996ff0992c58310d35af61f72c523aedcc7adaf42bc7e044d9243433)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6bf38e9f7ef19a448520647e48b645ef371964b8cbf4629878bfed2056df39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218fc7bce64182b443f220d85d2338e05406a37fe6c73620a7d1c57e97be0f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7baa29f47a0e222c8d03629479a9e2bd0935291fda5c1e07490b163eed21c13d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumesSecretItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumesSecretItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumesSecretItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a26dd922f15305330cfd0e91c74e640bd371a01d66ef6dc2d577f3797040e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateVolumesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVolumesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c162eb1ad80ed01ca8a5eb13a9d52cde3d5e0dc787999f0a36fb00a6a2916046)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5906f79bc9e9c9e61385ac20096d3ad29fdb21cbc80bbfd17da53d0a774635a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetDefaultMode")
    def reset_default_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultMode", []))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudRunV2ServiceTemplateVolumesSecretItemsList:
        return typing.cast(CloudRunV2ServiceTemplateVolumesSecretItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="defaultModeInput")
    def default_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultModeInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumesSecretItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultMode")
    def default_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultMode"))

    @default_mode.setter
    def default_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472d5a03df85a22cb54b2feaef9800d72deb4f9840b394c0161791b28e6600de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f4e12fdf89947d374d73dfd071e68b5fb4a4b3908d37ec2018d8ba05702151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTemplateVolumesSecret]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVolumesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateVolumesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5757a2ef6f28ca6526ddf0f187868f0e690193725747f23d8f4cbbd27c10c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVpcAccess",
    jsii_struct_bases=[],
    name_mapping={
        "connector": "connector",
        "egress": "egress",
        "network_interfaces": "networkInterfaces",
    },
)
class CloudRunV2ServiceTemplateVpcAccess:
    def __init__(
        self,
        *,
        connector: typing.Optional[builtins.str] = None,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connector: VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#connector CloudRunV2Service#connector}
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#egress CloudRunV2Service#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#network_interfaces CloudRunV2Service#network_interfaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f42fb82a7ad01240bf707df56e648b45671de77e069ab2f66871e779b9ebe3b)
            check_type(argname="argument connector", value=connector, expected_type=type_hints["connector"])
            check_type(argname="argument egress", value=egress, expected_type=type_hints["egress"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector is not None:
            self._values["connector"] = connector
        if egress is not None:
            self._values["egress"] = egress
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces

    @builtins.property
    def connector(self) -> typing.Optional[builtins.str]:
        '''VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#connector CloudRunV2Service#connector}
        '''
        result = self._values.get("connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def egress(self) -> typing.Optional[builtins.str]:
        '''Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#egress CloudRunV2Service#egress}
        '''
        result = self._values.get("egress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces"]]]:
        '''network_interfaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#network_interfaces CloudRunV2Service#network_interfaces}
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVpcAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "subnetwork": "subnetwork", "tags": "tags"},
)
class CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: The VPC network that the Cloud Run resource will be able to send traffic to. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If network is not specified, it will be looked up from the subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#network CloudRunV2Service#network}
        :param subnetwork: The VPC subnetwork that the Cloud Run resource will get IPs from. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the subnetwork with the same name with the network will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#subnetwork CloudRunV2Service#subnetwork}
        :param tags: Network tags applied to this Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tags CloudRunV2Service#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__952c23e4a0b7a5bdb85e9e0af9d6c2494193aad576d5085ba4e830769ef6b22e)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The VPC network that the Cloud Run resource will be able to send traffic to.

        At least one of network or subnetwork must be specified. If both
        network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If network is not specified, it will be
        looked up from the subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#network CloudRunV2Service#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The VPC subnetwork that the Cloud Run resource will get IPs from.

        At least one of network or subnetwork must be specified. If both
        network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the
        subnetwork with the same name with the network will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#subnetwork CloudRunV2Service#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Network tags applied to this Cloud Run service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tags CloudRunV2Service#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45d3d8c6fd792af233330cd290cff8d680bea389d671f7da9b0f66071541a5ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f167906c1cfc3859326bc8c48d72c4bf1075184c463abd5629456be7e1f12bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7aedd520e46a4ab9c33e8ca12070239b241c767eeaa9d8583ed3bdba9848b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__747f2c35a71a76934081d477665868060ab36a3a7106355d0a6cb8e4474750bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f7b3f4ee87fae1f36628cb4ca3ff4f6990bdb747a0d6933d05f03e04005e387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb545d5c58d17f4e42ae4f57d85b5ad8621617d5baabddd19108252123a0346d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a14c900111e8baaf16deb4e52d156d0fb138b6e1298651d720c8cd238af641)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07ca624d05b181ea33ac5c3d2f7525cd7205d532f4d73ea57f1f0ddd56a27ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9870533bf6de5f65ca5eec3f856a71774de9ac2c498797aa1bef32ed9d7e8fdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a5e19c4fd104459ef012ee5894950b22023d10a733ad0a4b9c586d0ca21969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99556335da45a39d6e2cd52c785095627e87fbe1d15641c626b1e0f46de355c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTemplateVpcAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTemplateVpcAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9030376659079e7437770a7083250c7e7549b41b9d9778d76dd5fcd125f5c838)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdab9231da9007a5b2381fd9a2e00163c6652a27173b19281a134b1712be3195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaces", [value]))

    @jsii.member(jsii_name="resetConnector")
    def reset_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnector", []))

    @jsii.member(jsii_name="resetEgress")
    def reset_egress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgress", []))

    @jsii.member(jsii_name="resetNetworkInterfaces")
    def reset_network_interfaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaces", []))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(
        self,
    ) -> CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList:
        return typing.cast(CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList, jsii.get(self, "networkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="connectorInput")
    def connector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorInput"))

    @builtins.property
    @jsii.member(jsii_name="egressInput")
    def egress_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "egressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfacesInput")
    def network_interfaces_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="connector")
    def connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connector"))

    @connector.setter
    def connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237eece4d565b327a72b86b5f671361602822d0acfd71a009e5cbf0b35d3cda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="egress")
    def egress(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egress"))

    @egress.setter
    def egress(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3975dc7ef737f38d97f89bc022d05a34bc7d73192a21f0297519ff9b0b356d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTemplateVpcAccess]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTemplateVpcAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTemplateVpcAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ceb55a63bf3d019062e6ff303e3f7f2309cea12eb8a46411e5d42ee8a96234e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTerminalCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2ServiceTerminalCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTerminalCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTerminalConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTerminalConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c512aaa1f6af289d9f23312fc1901df1d1be04e7936c34285becab628af3317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTerminalConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ad49e425aaa7769d7a518deb97e6b42bc3ef110415147a1380e6401ade6adc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTerminalConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb6d8b057044af40136653478b7149b0a83c7881819102f7a07559c551448ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76b3e98d4e1a48d89bf65d6ca3aafbeb0342700d80e6a8b6430f00b195ff4440)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d29d0471345c7084f2cee9154e7f094775b4c72bdfe6e8ef9efe426e82c86ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTerminalConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTerminalConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9505ade7e7f4c83704eec5ea6c85a78d66cf8a7c65bd42b44bcb170ec0636672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="executionReason")
    def execution_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionReason"))

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="revisionReason")
    def revision_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionReason"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTerminalCondition]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTerminalCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTerminalCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d421a78a2c59a1e26d75d799c9d502137045dfc42e5b34006f8a51f7a3c34ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudRunV2ServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#create CloudRunV2Service#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#delete CloudRunV2Service#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#update CloudRunV2Service#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716193324c7e9fda1a33e7036fb45c5ebff6c575a8626dd25d76eaa8b95502b8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#create CloudRunV2Service#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#delete CloudRunV2Service#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#update CloudRunV2Service#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__172634dfbd21209c37bf12a8db1eb033ea891a0b276a5f092ad17942d775be97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a4abf672b1109c78cda423d0504ef68fe1f8d5b85cf1f39a72b2715c9c42699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6f00daa48a8d87ddfa099917f8e042cd45f8be1d3621872fe3db53bd3d4fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7073b0f8c8aee544cd260f267da3e19cdbe060843895a0107ed0e2b2c30a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df550a3117f79e1c74fd7cac645c779a705eeff4257b022246a00335fd2fc7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTraffic",
    jsii_struct_bases=[],
    name_mapping={
        "percent": "percent",
        "revision": "revision",
        "tag": "tag",
        "type": "type",
    },
)
class CloudRunV2ServiceTraffic:
    def __init__(
        self,
        *,
        percent: typing.Optional[jsii.Number] = None,
        revision: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param percent: Specifies percent of the traffic to this Revision. This defaults to zero if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#percent CloudRunV2Service#percent}
        :param revision: Revision to which to send this portion of traffic, if traffic allocation is by revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#revision CloudRunV2Service#revision}
        :param tag: Indicates a string to be part of the URI to exclusively reference this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tag CloudRunV2Service#tag}
        :param type: The allocation type for this traffic target. Possible values: ["TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST", "TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#type CloudRunV2Service#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b9883fc337ef80fa9a9c32cb88865986e92196d607efc5c18664fc459f9b6e)
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if percent is not None:
            self._values["percent"] = percent
        if revision is not None:
            self._values["revision"] = revision
        if tag is not None:
            self._values["tag"] = tag
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies percent of the traffic to this Revision. This defaults to zero if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#percent CloudRunV2Service#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''Revision to which to send this portion of traffic, if traffic allocation is by revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#revision CloudRunV2Service#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Indicates a string to be part of the URI to exclusively reference this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#tag CloudRunV2Service#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The allocation type for this traffic target. Possible values: ["TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST", "TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_service#type CloudRunV2Service#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTraffic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTrafficList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTrafficList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef12ac5cdf669de02c606ddd7d540e0164df447af5c9c9993390aef1f6df924)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudRunV2ServiceTrafficOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a885ba722710dcb5c902993b4b1be734aaacd1fcb68e0fd0016752d40c2106)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTrafficOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8945ecbb2dd3e0eca22cb3c449db2f6f357244dbca4a0e7b48af7231afe3b7f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1da1b09ae0bdcaf68848bd810c4cd90942f810c9f0e55ae841317c5bacb51ab3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de94f08dadb96bc5d8231e66a9f63327fb8c879370439a3ec63f6cbd8527cde0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTraffic]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTraffic]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTraffic]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160da6a2d3cb42960bfd080152e723cef1577d94f3210641c90e451101c7076c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTrafficOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTrafficOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__375852cb72dbcfcc3b0765a8b1326dc262c4622b0db6333cab6e76c6965f9fdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @jsii.member(jsii_name="resetRevision")
    def reset_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevision", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2476ed6d9968e2379fcc421b4bd0a6bc1d258c76a1f1d792e95ac766f451b20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca1dbfb581b96683df1a0cd12b12f624e0f8db65e1a53f0263c23db6a84356b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1783694598e5bf64ed52316adeef2f6de269abe1878e0e83dea1be256cb46edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbed65afc07302f6332514333d8c391f79985345605514ab9fac7a3ad151e80f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTraffic]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTraffic]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTraffic]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df594327801b90bf9a99fbb5d8b71aaf878e03b0c09aa07a8746a0511d838814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTrafficStatuses",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2ServiceTrafficStatuses:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2ServiceTrafficStatuses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2ServiceTrafficStatusesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTrafficStatusesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0eff4dcb3bff9b24dd1446c935c9ec7ee6ec78bc5fe51084de469937e66092b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2ServiceTrafficStatusesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370336629fcd568c44bce9fd0a027662c93976d45def7013d5e9a7590c9bc990)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2ServiceTrafficStatusesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a02fe12c6e078f92517979c110aacb7b72376ef2a4258034161e79b135fcd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd01e21b367a4323da32f8f52ddd0d7018711b81efb1a732cab2ee89225f5976)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7100013a2c34c2a55857cf91cb6b43b216ca3ddc0936a60c96d346c3ed5ae18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2ServiceTrafficStatusesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Service.CloudRunV2ServiceTrafficStatusesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df1f9f8a7fcf92e990d7037aaf445b874576b695287f5aceba5b1bf401aba487)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2ServiceTrafficStatuses]:
        return typing.cast(typing.Optional[CloudRunV2ServiceTrafficStatuses], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2ServiceTrafficStatuses],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269988c38269bc38438e0cf14a5b904cd15fb1b3586234678a52145b374c0be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudRunV2Service",
    "CloudRunV2ServiceBinaryAuthorization",
    "CloudRunV2ServiceBinaryAuthorizationOutputReference",
    "CloudRunV2ServiceBuildConfig",
    "CloudRunV2ServiceBuildConfigOutputReference",
    "CloudRunV2ServiceConditions",
    "CloudRunV2ServiceConditionsList",
    "CloudRunV2ServiceConditionsOutputReference",
    "CloudRunV2ServiceConfig",
    "CloudRunV2ServiceScaling",
    "CloudRunV2ServiceScalingOutputReference",
    "CloudRunV2ServiceTemplate",
    "CloudRunV2ServiceTemplateContainers",
    "CloudRunV2ServiceTemplateContainersBuildInfo",
    "CloudRunV2ServiceTemplateContainersBuildInfoList",
    "CloudRunV2ServiceTemplateContainersBuildInfoOutputReference",
    "CloudRunV2ServiceTemplateContainersEnv",
    "CloudRunV2ServiceTemplateContainersEnvList",
    "CloudRunV2ServiceTemplateContainersEnvOutputReference",
    "CloudRunV2ServiceTemplateContainersEnvValueSource",
    "CloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference",
    "CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef",
    "CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
    "CloudRunV2ServiceTemplateContainersList",
    "CloudRunV2ServiceTemplateContainersLivenessProbe",
    "CloudRunV2ServiceTemplateContainersLivenessProbeGrpc",
    "CloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference",
    "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet",
    "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders",
    "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList",
    "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference",
    "CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference",
    "CloudRunV2ServiceTemplateContainersLivenessProbeOutputReference",
    "CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket",
    "CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference",
    "CloudRunV2ServiceTemplateContainersOutputReference",
    "CloudRunV2ServiceTemplateContainersPorts",
    "CloudRunV2ServiceTemplateContainersPortsOutputReference",
    "CloudRunV2ServiceTemplateContainersResources",
    "CloudRunV2ServiceTemplateContainersResourcesOutputReference",
    "CloudRunV2ServiceTemplateContainersStartupProbe",
    "CloudRunV2ServiceTemplateContainersStartupProbeGrpc",
    "CloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference",
    "CloudRunV2ServiceTemplateContainersStartupProbeHttpGet",
    "CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders",
    "CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList",
    "CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference",
    "CloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference",
    "CloudRunV2ServiceTemplateContainersStartupProbeOutputReference",
    "CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket",
    "CloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference",
    "CloudRunV2ServiceTemplateContainersVolumeMounts",
    "CloudRunV2ServiceTemplateContainersVolumeMountsList",
    "CloudRunV2ServiceTemplateContainersVolumeMountsOutputReference",
    "CloudRunV2ServiceTemplateNodeSelector",
    "CloudRunV2ServiceTemplateNodeSelectorOutputReference",
    "CloudRunV2ServiceTemplateOutputReference",
    "CloudRunV2ServiceTemplateScaling",
    "CloudRunV2ServiceTemplateScalingOutputReference",
    "CloudRunV2ServiceTemplateVolumes",
    "CloudRunV2ServiceTemplateVolumesCloudSqlInstance",
    "CloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference",
    "CloudRunV2ServiceTemplateVolumesEmptyDir",
    "CloudRunV2ServiceTemplateVolumesEmptyDirOutputReference",
    "CloudRunV2ServiceTemplateVolumesGcs",
    "CloudRunV2ServiceTemplateVolumesGcsOutputReference",
    "CloudRunV2ServiceTemplateVolumesList",
    "CloudRunV2ServiceTemplateVolumesNfs",
    "CloudRunV2ServiceTemplateVolumesNfsOutputReference",
    "CloudRunV2ServiceTemplateVolumesOutputReference",
    "CloudRunV2ServiceTemplateVolumesSecret",
    "CloudRunV2ServiceTemplateVolumesSecretItems",
    "CloudRunV2ServiceTemplateVolumesSecretItemsList",
    "CloudRunV2ServiceTemplateVolumesSecretItemsOutputReference",
    "CloudRunV2ServiceTemplateVolumesSecretOutputReference",
    "CloudRunV2ServiceTemplateVpcAccess",
    "CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces",
    "CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList",
    "CloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference",
    "CloudRunV2ServiceTemplateVpcAccessOutputReference",
    "CloudRunV2ServiceTerminalCondition",
    "CloudRunV2ServiceTerminalConditionList",
    "CloudRunV2ServiceTerminalConditionOutputReference",
    "CloudRunV2ServiceTimeouts",
    "CloudRunV2ServiceTimeoutsOutputReference",
    "CloudRunV2ServiceTraffic",
    "CloudRunV2ServiceTrafficList",
    "CloudRunV2ServiceTrafficOutputReference",
    "CloudRunV2ServiceTrafficStatuses",
    "CloudRunV2ServiceTrafficStatusesList",
    "CloudRunV2ServiceTrafficStatusesOutputReference",
]

publication.publish()

def _typecheckingstub__7f648a6d9fe5b20c0bb2f5645b46ae9978684d7f9cd4b499b8f94bf209b42889(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    template: typing.Union[CloudRunV2ServiceTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[CloudRunV2ServiceBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    build_config: typing.Optional[typing.Union[CloudRunV2ServiceBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ingress: typing.Optional[builtins.str] = None,
    invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[CloudRunV2ServiceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudRunV2ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__175ced8f1ce80e2c520e73dfd55d7418b8daa5da5480ed413835d096e1611c22(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342084dcdeb5b28d579e5f6c58cc182c3151b6cc29674e39fa2bb317a1082a2d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTraffic, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a888ebd91dccd3ef5c8c832832fe2fbf99f85f96b43ff410dabea674a4325a01(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36047ff638d6b5924690ddc831560c91cade2769d4e2e13641e9a4b024c4612f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b56c66002d4aaec7d99a76ebc39b64652968e45521c9e42a34f23712ad68d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68fb9a0be296e7f48c40d4b23f927b7a44eab44a25d1684780d4ba2a5e3f726b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81697b62950a249967b374477b3e194593be693e9cdf5245a76035c03631a1a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6767bcef21d80234e4fde68727d60f0b033791cc2869fc24bad7be256cb96209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15406630f376c4f75132ba2257f84b69f22b873269dac5a462e4254797f7f752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0a37206e05abc3e38b9045f0014595d52b472281b61300392863afcf0cc14f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa1a40fa285556246951bedf735ba2c0231d6bce4f6e44d1fc50df7aedec252(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c563227b75604cd3cf205483eaa37595751af7e8aa8c2d57dace8d5f634df1f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e3d6aaed401c99c67bae47c21b430e7d068469da976cdc3fd556e00947a352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2535d080a4042b5dcb4d18d8d586d82b9ecfd6dfed78fd592417d39b132d7023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710f6012705175c08b1141341778cdd64e131b091c48ce49d82830dab9fbd1eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ebfc79cd9a40c0316f7f6d97c366e16ffb8e0f2332e4b15f5eb476d03562d44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98bf701aa0ab33be1b50f9e63713e5f6262566a7824c223c938dce0b52351f2(
    *,
    breakglass_justification: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dcbf276cb4df159682177c47892ddb850fd2ac2770c84685f520ead0381fbff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50264cb8b9edf787b5117d4beb8725487c876dc03c8a2c282f6c09cf346bc56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a41eaa16ce86039b4271824be584f777cadedc6e01a4ff916e4377093a35809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c293f0f4b74393065b50ad1000ebb801609962195125b1028140d125acb254(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f78daabaa8266f48b310977f18ac33a83f41a7412185d3e225cd9f38e5b2f74(
    value: typing.Optional[CloudRunV2ServiceBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f52c1114aaf4ac96ae62aa799e11605fdfa6146b957383fea9d30841279c17a(
    *,
    base_image: typing.Optional[builtins.str] = None,
    enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    function_target: typing.Optional[builtins.str] = None,
    image_uri: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    source_location: typing.Optional[builtins.str] = None,
    worker_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5515a9e10807d68fb42905bd5d982d4f527f2272a2009c3fa668a073704f31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fff98a91a613aaf7ec4c285f54b857bd5b271910e1eed726797724fc60da585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1486d6aff57c6ae853b4f444c0aed017ac5a60dd82264594d46e7961e31ef917(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b97f58b9ce4d0412c43501d546782c3a9787a8c2ce8478d294fcd5597e39e73(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7775364b3f8228d27ac3175f01c9f55c04a23159f4687239a4332b33539a6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3e0ca4f341a96b053fd0ba8a240aeb6fad67ede21bcdba14a64025963bc5d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f0d4e19f4ba214943ebfaf8e43097829222953f20260449b668d5078d56fe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b38c077d279539164c76448b30de0f3f6189ba3e83dac3da4dbc9e0e9fcd91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c908890d70d8e11ee420239850a7771e9ff73c9ddec3ba00917b393eb381c5ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a9a477090be0cd89d63cfaaf0ea164fa535c1ac49bfb3984fdc640d6a515db(
    value: typing.Optional[CloudRunV2ServiceBuildConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2c410b6b5e91f359844872e2d53e132bac5003f9ddcbbd5a3bee1131d3f77e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53217eb0573812a99323f60f5e7f83dba2bdd9f010ac41d14ac374da9f55007(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c138c8a4c0aaf23a80da766270066b921f69f71f57bd2d944864dc5b93d1ab86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f1061a1758860c9ad8d47911cf33c840263c294a03faff97ff1155fc684260(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1069e7b106044e36d1d3f375f2703e5887c60b085353263790de3277bd25bd16(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa62713a40a8a2e5483ade04e5ee98e1d1403827d00e01ad9335f5210050a8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8a263326f798303080419fe029a2dd97dea09f2403280c346b4e8e7bbacf6c(
    value: typing.Optional[CloudRunV2ServiceConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0014b5e160c040f73cda4019aa150a8fc78aef2b68cfeda3ed6a8efcc1b071f0(
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
    template: typing.Union[CloudRunV2ServiceTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[CloudRunV2ServiceBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    build_config: typing.Optional[typing.Union[CloudRunV2ServiceBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ingress: typing.Optional[builtins.str] = None,
    invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[CloudRunV2ServiceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudRunV2ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c7a86c3f9c282ed6076748a69464579370f6bbbba04519875d2d00fc68fd23(
    *,
    manual_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    scaling_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd5742acda2fd46c8fc7abd8ef6f04bc84b248ab63e36bf62564de55b61dfce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b575cd72d760ba807e4c37ec1ec8f75b2379315e530a1c6eebfe4988fcfb442(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0401e737630b7274e2515e5f016f425b8811847727b603a4580ab8ed07bf682b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8811b18a4d992037688b2b4d997450835ee52f9ff488c6de7acca28db0278ab3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1174cfa446945167b17f9fb31568c5a7d1d69dde13bf57329142f4491449fb(
    value: typing.Optional[CloudRunV2ServiceScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d3bfca5e54a4d398ff775e01c980d9bced7479c7d0e1f004555612bf3fed1c(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    execution_environment: typing.Optional[builtins.str] = None,
    gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
    node_selector: typing.Optional[typing.Union[CloudRunV2ServiceTemplateNodeSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    revision: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[CloudRunV2ServiceTemplateScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vpc_access: typing.Optional[typing.Union[CloudRunV2ServiceTemplateVpcAccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86329e372ec653fd4dbecd19295fcd59fb3469401986cc665947a12287e3d34c(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    base_image_uri: typing.Optional[builtins.str] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_probe: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersPorts, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersResources, typing.Dict[builtins.str, typing.Any]]] = None,
    startup_probe: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e987b8443520d78f214d89d22153a16202862297a0dd3ad3dec2ff1f8ee01942(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fc45fa5526e97a3d1e65ed05282e74390b428dc008c9e99430e3a7de142b27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96687a146237c0828d5d7c7c12b86d573f827f7133b9dc7ff6b668a5941b863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79327edcb318d46f7f33ec19cc9e69f650c386a41a77dd479e52a60ccdca4cc9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ffe278e87e01c6b8752cd8f9d1ab1eb868b3bbb64549281a1d9900bdda49266(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afeaa7f50238235ba56d47af09e9f302f7e826e5802ce50c53276ae53fa4d56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8247a7903111c1847148e2c74ab73b1c8615d7f921a47f793c5c733859356e8(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersBuildInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcb3dd8d3e3abb15f91d9bd100bf1586561281aecf86a24472f10f87befab38(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
    value_source: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersEnvValueSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd16a4c06d3f1713dbb452774367a57addbdc8d91e6d793f1ac9d261dcb594d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f09f645eaa708490788d7e70648806dd23222978e0ebb0dae32444b2a6529e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a462e097ac3df2ad09425fc79157264034c1f31d50dbbfd2c057873b28d7556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8778ceeaff98c08dd4dbcd5ddf3cf8302475ccbe86e362dbb215cd5df841215f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12b1a69187e3506f84279c3ea8f25810fb43ef0f63a300ede713db12e90909d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e86ff8627d05f2da0d4344f23f0a42c401b2566c0cc7ef702684d715b4aa6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e923eea11fb11cf64f3c795d1c449e5eaa57ec9cb1802e939ce2792ebd42d9c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4a2c5a3e9cb04877002136d98867a4a0fcdb52e9cfa28d61cdbb198b201562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe47175d6d6c47416df98a5daa04fc224787a9dff8d344e507b8314df64655b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe56c873c84cec931a1179f226dd17ad2dfbab1f30930f8eef7825ba454288e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfee9b8c4add18efebba832664f9b448af80c724b4f05f057b8f65a1179d01f(
    *,
    secret_key_ref: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae2d66fa9e69f53fcb54a159608bf9a966668577358182e268e8e0fd9d24357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153e41156d83cadfa414b4567c5cb0bc8a94877627861d881dabcf007caea063(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d635373b9140e0dfd31a4e7f3a7b80c11182c2f8308cfcb2c10b84cc990931f6(
    *,
    secret: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c70a0c572dd75e750d6db2279edb636662a78ce06d127b4d028f535ddd13b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e2beee642ad85b50933ebb057a0e1a53c7dabbadc8b7206707e634c663c34d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5968add9ee1baa40915be34c24bf45481f71cb66508e38951cc11f9e521f85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c36ce0b21d76181c96d6894bb328b12f1b0ff7ddb77cfdf64f359fcb471bc86(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1189a1c7d59bb30a3bed145c98e910a41b6014113a86307eeb78124c57c904c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21795d6278af2e47bb893d9016d873226a993250d82cd5ed3cde216b2eb96c46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143f2b81f929a8e219c06f8570bd794d0b86ff98d0e5bf5477c70f85a9092e91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83f53819fe49601ce199a18afbd106ed9a18341032e5aa7df62b4837527c704(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc13b7cc3f684f0a4e233c818e8e72dcfc0b083f5489c305ea853503faf5146(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d685c248fe4da1abb9e6a1439041442724194417a41039494d342d322e2389b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52275fafcd3e7caf04971686c6905b28f5ed6b94eb125b4c3b92548a627216d(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c9e7a7f06cffdd5d46ab0da907df48ac8da868109891497dcad83befdf4166(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687e10d1a428b4a29d3ac604c229ccc3725b2e5e7626ca21067c9084408f2fed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068d7c0bfc6af11d2f7511c1946ccd64c25447703461237af9da79e4c3f35b6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb1321c7b28ab7272a3f50ee0969286b7c9c9d5c5c40f4d377e8f2dd09c5b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fda1dfdaf8634723a48b902c4fdc2bafc512b2b6906f8dd488822b96ff479d5(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a41601b4ce807560c09857847be36887e4351504a0ffead63acc54e831d57c6(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c64d7551982d384af893a6dd5b9a1917dd28917b65b3b0dbfde3753bedfb2c0(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458df13be69532b2a778dca0cbf13fe4e26765bacf1341ac02a9a1adbe379832(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9428300b40634e8a2146521ab3ebf1682a9cd9b84878d346bab3c64d20fe80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950a6e490203f8aa931666a652e9081b8e0f3b01aa80602c5200423d024faa20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c68a6da08fe2d10fa2fd2f7cc4a98fcb73f4fb62790823fdb9eeeb94e01cc8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a2f0ff679b7f5905468b0b170e372d339e76040ceb08a83efe3c4ad530f99e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf138b91906352d98fcb887aff6222ccd29d367f61ba1bb641f0224d065d912(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c192e599dc8036cf03aea3768198b1d5914d80aabb7762cc83a111bc1cf2083d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b34c90d685ff838b09de91b27ff7135e63e8aa1d6b38743db662ec15c6c0fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b21f353364275bf49da1b6bd00a601bb4d2ab8d7037c4e19185f5f28c2e546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0253524c4807719afa70fbdc1cb0a0cdbaa02ddcc7ac8a54c176aa15280edf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42655f0df5f328c995ee5ffdba55af8681e32996e20dcae768c668dbbc04272d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460da7085bf42824c45af26e124b91eab92f326e23c982b051c9e3f7bcaf4228(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef55fb24ca5590fcb5cb122cc15373ba955573252da58b92f9a6f3b1de639e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d7199056c234b78183e7edaa26b812a498e3d7a6d28a2e7a463bdbe860936f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beea5a8b9e375aa215f3a776f24d820bface90610a532f181e6ba8213e1ffca(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9930ae9371c403b2b8ffba4cacdd50143efd1e5d86547b2b958b63b4498f520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702ab29382c0470c6588c60456cadbbd36a4ab3969ebf801b57ac48e9ff00ae9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e95ae97e94b30666475ae4790a6a29e2dea16b0f36f54e17f6c82019c1f9260(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac28a481005e129553521ff682043ce2ab8468b44c72f28422fd31b3d23408a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38aa3073d036fbcfaccf2dcba7a662365afc89e507d98a3280792fc3032fffce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec53bc311869dbb6bc76b176cd1feee77a57bfeda99f6800ea773fb285251965(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50268e56be1e9096a04e10de375aaae39dd5489e659ae97a8ea916709ae9b4df(
    *,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ce602198b5691dc08bcc3d616b6156e0c7b13dfd640e2861b53ad727099e21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b4bcef94a2e3f694a8831d71e0c590057dcdd14d02b2eb05a07b155977003e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b92fc43daa7df77c3a7620c1a37d452477db2739aed953d2176bbe003e1060f(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81bc1af1490110259961e18236df3e92a26a37ca6fd3389b793eebe01476d195(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61b51bdfaece5a30695c6cb667c13a54a5aabdd47653861e2bdfe0c56d8cf7a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e78cb6f27530c26e24715b25484a9a03b9bfa56529ed66eadfe36409dab284(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80eeced003b878b2746b8f290baded961bf47ac5d1ef6ec758c29d4079e8e23f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71632689be500bd2bdbe5d53569065a4025110dc0d1eb6c5c57c6401a23791f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9ff1924dde182574f947d258e0db6b4f4737e889307ef430be180d8c4dc273(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcf159f9e2908c8115bbb65a2d9e78b5b62cd28e2f2032f41db9b84de3e4644(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0deb5d61f4a6234a6cc3d78ec7c4356afbff25ad699dbb30873484a6ad8634ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0307679ae2963708f7e3047ded1d33538dca4475693c2f27689bf63efbba1a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c631de891cc696b6612ec7bbbab22f293c79d7dcc5799819890df763a800dcb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121df78a03ec00928c88ef68b7e63bbacba280975faad1581cb414bde5cf3fa5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23de5fbdb1a131c1121443263fcd0f538e3a80d6b1f01e57c0d55dcf8136376d(
    *,
    container_port: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15980028acf2fe3f6f90a259cd5104622094e29d2342e1ee2f7ad7ce7e334426(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76559724f4fb7bd5dc88000c653f71f5c2264d7272b64c2d389500fde510373c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dba8a96945ab8684bfd2410baa8627a8685182bd529ed46d886cc851578951b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f99dc3baf3730e7f87a0ee43f55c5c924d9a25d82ddfbb9e8be24fd51843e34(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersPorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170b8a4fb2157a238737d366cd7c416ba8eb444e4daed3859935310674a49f61(
    *,
    cpu_idle: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    startup_cpu_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef5cd008c0b5cf424e4df15dab4422290fdbd09395902e8910415d4587494d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb0ce3d4493ab3867c7982292fb1319d6b645c4821d789f2832b197104b9052(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85888149006d451fc648cb3834510c09ea1a084ab80c58735c13c2f692b737e5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b6a3741556cc5de2208e4a55fb96af3a94d2d5d683ccae93dce9adaffd94b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dc67d8a24219b8e5953aee02e73595e1631d9cc84412451b2704a1a66a25ac(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66729538d9e7414f7d58e4480760575ecf0a7787f3d6796ae46a770fdbeebbb(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8232faee8feeffdd572bc194c82ce02d9a8255068c7df085c5e41b9998405d23(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51168a0c7843bd214ceffa916c1296c790f0cbedca9f7c30344e312ea4c05a62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9f0616dab5f3afb74979f879a954506bdbfd939d3a1a6704e38f63801db664(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d774dce998e527d95a770fa3fce2064287fb0c039e3d5eaa76583abc119855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ca85563d394a4c2c0bd43fa090b91da33883f8564bf5030418670bfee02452(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319de96cd4fd21045e6bc211ee50fbe3a5afcdbce57ef133b7df59265866f0b1(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad8bb5565393dd68347af127fa0e591642ad5a10b9c8a41612ff8e4004a9c35(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6593775bedd8328ec9d4f67793a9e033ca0fda163469e597c166777ea040eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c847a9ed5b99588d67f78d5fd4c9d4e244a02eee20b2db8ab96c83e3b9e6a415(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484e350d74384436a6da9e927ad72253da1e3240aa010f1cb5446bea138998d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2852deca235aea8096ebb8caa5d44e8c4eae23248c85f43a24d07a071e25b2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fefea252665cc57cc23246d7512c149d6c2a84e8fec9a6dc0d9cbfca260562(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9732be975b5f765c6a332c953d2393b21b597f39007ab036b9c16e0d10e78e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b256ad3b332fd9d345308427983f54bf2b051b0d1d16cb82b899a3997ee37e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc5bf6fae3108f32a303bd5ebb84f37079c4be2fa2994b66d9a3be3e4753dbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5110e707c9e78ba18d6787e1e4d65f7b61e932b76cece0fc2bd3486c0b94378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c38db02b6e17b228591a854673af6fea2d3ff5d98f04e2365efb48d062cf743(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc89b55938de68bd1cb9300f0fcec2aadad1e0e169a564fdd6d6da96edb201f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b330b30f1317e706935704e2a2d2892ee862a210dff6ab27c331ab6ec4c1ac6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2ff699f5fd8f7f99a94dab4495e2749cabf2af7253a5af33ba2de186606b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d80edb49872fe9995f42c285e47c673cd9d4bc87ae530fe5afe0a5846a46fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa344877b1b12dc753134195a46ea5a97b75aabc4b38500765055d07c86ec42(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877f260601b1d9059466ab5f367858051d7dadbeb0c3fa33d76c181180887a43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998218ef6f620b60c2621fff442d60e1218bc90264f4a03dc05572ced612b1f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d79f7604cd0888c358b03a86d45072f1896c2d2b7af86e57c7ca1a0f1e3ee0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd0cfd72a7c2d19dbe661b8142a34170faf879be41290986f6ea7bba0bb8b73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48d4186d9a20c76d0a77b162c3b8bd0d75a645d3f944a8c7538fcdb98d9451c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af576ff187d081a09f409b86016a2f981cef538757290b2c21cf80af2befc54f(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8648255c5fbec5568045e56df2a3da21083077c017bee63937215b431c3f89(
    *,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226a907a4fe33b080ac2286ffb90d598953fe0ea4453f47a4d20cbdc5de68830(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78859d5f0e2a9ee09fd32a613da4984798699aa0ed19a92e0b144523df3b51e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe64da29e82a74df5caa96c3e319efaa6369646bbe06b205ae28c87e9c8a2039(
    value: typing.Optional[CloudRunV2ServiceTemplateContainersStartupProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c249fc6e4b259c842313efa82e9077b9ce3fa6c4fffecc4e1b844e3d1b8cb04(
    *,
    mount_path: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a592bee5333c30d746a255edcf9a8f3b8a65f79200c3537b0cea42dfadb0a92b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fe114314e439aadcd91f20850a082d9b7104988ab954376241715c64814545(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8383744a8a923d186866a862e3d2b6326e325641a8a3bb90f70993a817eac14e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dabea0345d75428fd9998d45ae46e960177513a1057e3383092c08d48865f58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65241fa473cc33154e1cb8dc9a81f3e9f3b6148ef16450947c4642230b536724(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7b8d30a0a6b37f96cf2bf053edf4bac9cfc21eb6b64af98c39a136ce8fb427(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateContainersVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38794680763ca9839b37e85a7f47209b759c055589614dff66848637d0d7e9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b92de0b46994cb554e29fc1559fcc04c32c7d944492e7e1a4d82e985a914d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4467a78fcf2cce19b519774da0ff18ad850d7a8eebc9bbab75e2f4349e55c2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0857e048981e774020c2d62f41788cea4e99046c172073a83e5695a30810faae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateContainersVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bab498950cecffe0689454cf2eb496d7a9d81d88e9ad7cee5c80fb0c669f968(
    *,
    accelerator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806eee9761de2d6942e7b89739868e46e96f0a0713f02bba2833460e6a19839a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1158268841df715efb59508fb6d9cdbc6e17558efff9536a7b4f4f669bf23d7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d2427be2e2849c5010bb68a5e957c8166a618b448f7139e5edd1a25ed5c041(
    value: typing.Optional[CloudRunV2ServiceTemplateNodeSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf22ecc7cc1aa02345c743ff8271f9e8831da5fdd4d42c04ce6107e3c9869f79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4beb3bc9b7baceba5b29f95f3428ae2ec1fc001f5729024ee131f647f45e63b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7606affc926265aab9be20aba8bc206f8a0951d0082c31ee15b6c60c0d9bb925(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1f350ba78b4a40782dd1d8448b05b0580941364d87aafd8acc9e59f95f0901(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982aba328432493ea863ce14a9921564f4cc27acb246b652680efc3e7561b809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d83e7563016dab0cbeda86ce07d5b0593f9b57c77bc17f1a568cb1b5fec2e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca762004d9a772119e5c4023d793d18b0709ff24a0fb6199bf2557f4b241d4e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5e55d2f0aab0d578ea6930247ce9d3e86e84249ce11bfa661f14badc785534(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40c628bd08fadba4418d1860669d63fa89fbc7bba8b642fb43f70ab742d5c9c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7275914ef6e09e17400be2d0cfa0e4e4c1e6fd2bfd57819aaeecc723a8af24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc300c4e6da700f3583d6b01e4d6e2d64ca84e6ae834fa56f4e31687e3dfd367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9012ef50ee970d0c99678a61a11359884789457d1e35819f75267b7f77bd9356(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba86a093e9e0754232a3d3a1b6fe2864332487f0ea86184802023d4bc5013a4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa5a14d240c941f45735498dc28360bc111ed3af810cfb9637ec2c5c75578f3(
    value: typing.Optional[CloudRunV2ServiceTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e5d8beed9bf83e7dca58ad699539d772fcf63f761d44e78f8c7a124052cb73(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05543d3b59b21b2b97794e248048f3333c1c1554ff2ba120ac8cb4ff768348fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b008e985a52d4f6e4f5133861a4768a7118bbc27409fff3c03337017de436482(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c750587991b7a87f008fd76ae421b025f74b5cc05a90fb600c4d82b178d8f888(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb858aef68c03e8eeae0897378ec1b0685b036668c7284f1f3bcee6adafb169(
    value: typing.Optional[CloudRunV2ServiceTemplateScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b4af8d0c08ce6753e1dc6bcb6197154395aadfb247e9cb51e2223af888e9b0(
    *,
    name: builtins.str,
    cloud_sql_instance: typing.Optional[typing.Union[CloudRunV2ServiceTemplateVolumesCloudSqlInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    empty_dir: typing.Optional[typing.Union[CloudRunV2ServiceTemplateVolumesEmptyDir, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs: typing.Optional[typing.Union[CloudRunV2ServiceTemplateVolumesGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    nfs: typing.Optional[typing.Union[CloudRunV2ServiceTemplateVolumesNfs, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[CloudRunV2ServiceTemplateVolumesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c07b9c8d709404c3db5645e73c792798a2760baad4c3fa0b37a353a7fa8f5bf(
    *,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ae9d638833ad2b42e1e9a6742e298d3c7d8f02828944ec96cf8dbf9d4a4905(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ed89f402bf6b5bb790e614f1533f66b4d93d68ecd45d9368336c26fec2d99c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3b9c079d5e6677db8daae57207aeef6c15d7f160790795337a78ef3e01c421(
    value: typing.Optional[CloudRunV2ServiceTemplateVolumesCloudSqlInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b81d6657e220a8d8e8ce383ce73c0621a9f096f85b296b6ca92c8a12abfd69a(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dbaea608ef3c7537405bf8f8408f38b53700e7a788156245976ea95845f5f95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751fa55750d08d96ad318419cdd23f4ed6a13cc3ba8182f019fee595a0be849d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2005e4da648050e56ede564cf115c8e0f03288f67fd7df7e45ecc232056d572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a13ed13aa8a4783a09e8a4a2f27ede3092e4f25a6e9dc8890eab0f8148f478b(
    value: typing.Optional[CloudRunV2ServiceTemplateVolumesEmptyDir],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e166bf27d195036a7bf898c441a07060080a504448035ae1760f4c43e4808c(
    *,
    bucket: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f884e577e08a17317f72656f18e6b5e365f1a49aebe5a4dc1dc4a8d52de2c352(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d8b44f2975fdd418d6f5c1040d58b90c1ad9f68059e2e08f768d3747f7f3bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0502642fc858e4fc4d2413cb8a4e3f6f7960108cfa666872412f4a0e8ce075(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0080bbdf97ae78824e4abce1d15c552007f33f02df6ab6d626b6e1a19917ae5(
    value: typing.Optional[CloudRunV2ServiceTemplateVolumesGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8fbb91aed0776da440aec0ad605656fd94c16a5ee098f5503f0418b7c1e345(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7b708321d2dd8fdea88b041712b08521b3ce6c2529c5481ce0a2cb7beba879(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bd71e82d6e567a8b68468b5983f8e46f341a145052aaf9b083d5e5ff9521b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158be5e084baf58f6026678ee6fb1284e08de39fb095a288053b3ec94485b9c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06117ec160ff430de98cbec2d7d4ca30c56a515250a98318c0f74a64977034fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f472b40bc696a8958a213fe838ec2c648044af8f123d3e5951e80abb8db3e454(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab320416f93fd331f740dc41d0a9a8563956b2fefb7869904af50daed6b0f35(
    *,
    path: builtins.str,
    server: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffcc86bb646401f3e282c6e8c28c0c7ae6d8b63bf774283b9340da4deeff455(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4996bb1ec3fefdec5bab92cb295839904132f00603cbf08a756d5bd969ab034d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e5702b505944bbb7af619c14bb7bd836b940386508ccf59402071e6117246b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96705a74eda23d219f3f9d25d4d59066482bdb619133cb743c7f43f246c3a8fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b35a5b0c9f8c720d29ffcb94025d35fd38500cfba1c8626a158916302b2967(
    value: typing.Optional[CloudRunV2ServiceTemplateVolumesNfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bafc5d22b4c515d2fac5353e63d73fc1b1d34b98c521329deb02ea8f2b1f8bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43985a35a63a731a666534448183a622eb0f244dad1fcf0cc218b0ff5f0e6cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce5832ab4ebf33c32f85e20360bfe055a960a266a6937906955b8a3e89469b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c4a8a9700d249af53962509f2c043af9ce26819d5d499dbd94c08572587fc7(
    *,
    secret: builtins.str,
    default_mode: typing.Optional[jsii.Number] = None,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7287078e264ddaf9b2da735b8f3e9167f755933518d0168641f4b0f98f382e98(
    *,
    path: builtins.str,
    mode: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad674ab7150e54ae60def16177a399d098cb80f1370a31448a717bdd7b92d80f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b934e958cc729c248297f9ea8674849177bc70afe8bf365705c7b9d89251d31(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9cdc44c0e6a1949d42eae56b30bb466ab23d8f5e1b3cfb539ebeb570b5080f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5120128a0377888fa7c0b852ef0fa4c852aeb4a69eee8c83ef98ae36981d520b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1016326e9cc63a810d2e18f2825aa8cf154ba7c17c6d8b451e1bdfdccc5a9abb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc0d7076ad3e88e36d0cb7d170b122a1ea3e58cb18cfa8ddd27e9935c8c73d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVolumesSecretItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653f5f7b996ff0992c58310d35af61f72c523aedcc7adaf42bc7e044d9243433(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6bf38e9f7ef19a448520647e48b645ef371964b8cbf4629878bfed2056df39(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218fc7bce64182b443f220d85d2338e05406a37fe6c73620a7d1c57e97be0f75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7baa29f47a0e222c8d03629479a9e2bd0935291fda5c1e07490b163eed21c13d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a26dd922f15305330cfd0e91c74e640bd371a01d66ef6dc2d577f3797040e5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVolumesSecretItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c162eb1ad80ed01ca8a5eb13a9d52cde3d5e0dc787999f0a36fb00a6a2916046(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5906f79bc9e9c9e61385ac20096d3ad29fdb21cbc80bbfd17da53d0a774635a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472d5a03df85a22cb54b2feaef9800d72deb4f9840b394c0161791b28e6600de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f4e12fdf89947d374d73dfd071e68b5fb4a4b3908d37ec2018d8ba05702151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5757a2ef6f28ca6526ddf0f187868f0e690193725747f23d8f4cbbd27c10c2(
    value: typing.Optional[CloudRunV2ServiceTemplateVolumesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f42fb82a7ad01240bf707df56e648b45671de77e069ab2f66871e779b9ebe3b(
    *,
    connector: typing.Optional[builtins.str] = None,
    egress: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952c23e4a0b7a5bdb85e9e0af9d6c2494193aad576d5085ba4e830769ef6b22e(
    *,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d3d8c6fd792af233330cd290cff8d680bea389d671f7da9b0f66071541a5ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f167906c1cfc3859326bc8c48d72c4bf1075184c463abd5629456be7e1f12bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d7aedd520e46a4ab9c33e8ca12070239b241c767eeaa9d8583ed3bdba9848b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747f2c35a71a76934081d477665868060ab36a3a7106355d0a6cb8e4474750bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7b3f4ee87fae1f36628cb4ca3ff4f6990bdb747a0d6933d05f03e04005e387(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb545d5c58d17f4e42ae4f57d85b5ad8621617d5baabddd19108252123a0346d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a14c900111e8baaf16deb4e52d156d0fb138b6e1298651d720c8cd238af641(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07ca624d05b181ea33ac5c3d2f7525cd7205d532f4d73ea57f1f0ddd56a27ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9870533bf6de5f65ca5eec3f856a71774de9ac2c498797aa1bef32ed9d7e8fdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a5e19c4fd104459ef012ee5894950b22023d10a733ad0a4b9c586d0ca21969(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99556335da45a39d6e2cd52c785095627e87fbe1d15641c626b1e0f46de355c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9030376659079e7437770a7083250c7e7549b41b9d9778d76dd5fcd125f5c838(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdab9231da9007a5b2381fd9a2e00163c6652a27173b19281a134b1712be3195(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2ServiceTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237eece4d565b327a72b86b5f671361602822d0acfd71a009e5cbf0b35d3cda5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3975dc7ef737f38d97f89bc022d05a34bc7d73192a21f0297519ff9b0b356d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ceb55a63bf3d019062e6ff303e3f7f2309cea12eb8a46411e5d42ee8a96234e(
    value: typing.Optional[CloudRunV2ServiceTemplateVpcAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c512aaa1f6af289d9f23312fc1901df1d1be04e7936c34285becab628af3317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ad49e425aaa7769d7a518deb97e6b42bc3ef110415147a1380e6401ade6adc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb6d8b057044af40136653478b7149b0a83c7881819102f7a07559c551448ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b3e98d4e1a48d89bf65d6ca3aafbeb0342700d80e6a8b6430f00b195ff4440(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d29d0471345c7084f2cee9154e7f094775b4c72bdfe6e8ef9efe426e82c86ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9505ade7e7f4c83704eec5ea6c85a78d66cf8a7c65bd42b44bcb170ec0636672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d421a78a2c59a1e26d75d799c9d502137045dfc42e5b34006f8a51f7a3c34ef(
    value: typing.Optional[CloudRunV2ServiceTerminalCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716193324c7e9fda1a33e7036fb45c5ebff6c575a8626dd25d76eaa8b95502b8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172634dfbd21209c37bf12a8db1eb033ea891a0b276a5f092ad17942d775be97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4abf672b1109c78cda423d0504ef68fe1f8d5b85cf1f39a72b2715c9c42699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6f00daa48a8d87ddfa099917f8e042cd45f8be1d3621872fe3db53bd3d4fa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d7073b0f8c8aee544cd260f267da3e19cdbe060843895a0107ed0e2b2c30a49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df550a3117f79e1c74fd7cac645c779a705eeff4257b022246a00335fd2fc7f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b9883fc337ef80fa9a9c32cb88865986e92196d607efc5c18664fc459f9b6e(
    *,
    percent: typing.Optional[jsii.Number] = None,
    revision: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef12ac5cdf669de02c606ddd7d540e0164df447af5c9c9993390aef1f6df924(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a885ba722710dcb5c902993b4b1be734aaacd1fcb68e0fd0016752d40c2106(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8945ecbb2dd3e0eca22cb3c449db2f6f357244dbca4a0e7b48af7231afe3b7f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da1b09ae0bdcaf68848bd810c4cd90942f810c9f0e55ae841317c5bacb51ab3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de94f08dadb96bc5d8231e66a9f63327fb8c879370439a3ec63f6cbd8527cde0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160da6a2d3cb42960bfd080152e723cef1577d94f3210641c90e451101c7076c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2ServiceTraffic]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375852cb72dbcfcc3b0765a8b1326dc262c4622b0db6333cab6e76c6965f9fdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2476ed6d9968e2379fcc421b4bd0a6bc1d258c76a1f1d792e95ac766f451b20f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca1dbfb581b96683df1a0cd12b12f624e0f8db65e1a53f0263c23db6a84356b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1783694598e5bf64ed52316adeef2f6de269abe1878e0e83dea1be256cb46edc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbed65afc07302f6332514333d8c391f79985345605514ab9fac7a3ad151e80f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df594327801b90bf9a99fbb5d8b71aaf878e03b0c09aa07a8746a0511d838814(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2ServiceTraffic]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0eff4dcb3bff9b24dd1446c935c9ec7ee6ec78bc5fe51084de469937e66092b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370336629fcd568c44bce9fd0a027662c93976d45def7013d5e9a7590c9bc990(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a02fe12c6e078f92517979c110aacb7b72376ef2a4258034161e79b135fcd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd01e21b367a4323da32f8f52ddd0d7018711b81efb1a732cab2ee89225f5976(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7100013a2c34c2a55857cf91cb6b43b216ca3ddc0936a60c96d346c3ed5ae18c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1f9f8a7fcf92e990d7037aaf445b874576b695287f5aceba5b1bf401aba487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269988c38269bc38438e0cf14a5b904cd15fb1b3586234678a52145b374c0be5(
    value: typing.Optional[CloudRunV2ServiceTrafficStatuses],
) -> None:
    """Type checking stubs"""
    pass
